import json
import requests
from constants import SHARED_HEADERS
from datetime import datetime
from opensea import get_collection_stats
from secrets import NFT_PORT_API_KEY
from utils import find_by

NFT_PORT_API_URL = "https://api.nftport.xyz/v0"
NFT_PORT_HEADERS = {
    **SHARED_HEADERS,
    "Authorization": NFT_PORT_API_KEY,
    "accept": "application/json",
}


def filter_junk_sales(transaction):
    return (
        transaction["type"] != "sale"
        or not transaction["price_details"].get("contract_address")
        or transaction["nft"]["contract_address"] != transaction["price_details"]
    )


def find_thief_activity(nft_transactions, transactions, thief):
    results = {}

    # Thief sold the NFT directly
    sale = find_by(nft_transactions, type="sale", seller_address=thief)
    if sale:
        results["thief_sale"] = sale

    # Find the first sale after the theft, even if not directly by the thief
    if "theft" in transactions:
        time_of_theft = datetime.utcfromtimestamp(
            int(transactions["theft"]["timeStamp"])
        )

        # Traverse in reverse
        for i in range(len(nft_transactions) - 1, 0, -1):
            trans = nft_transactions[i]
            if (
                trans["type"] == "sale"
                and datetime.fromisoformat(trans["transaction_date"]) > time_of_theft
            ):
                results["sale_after_theft"] = trans
                break

    return results


def get_price_details_for_transactions(
    nfts_original, thief_wallet=None, victim_wallet=None, **kwargs
):
    nfts = nfts_original.copy()
    collection_stats = {}
    for unique_id, transactions in nfts.items():
        print("Tracing: " + transactions["tokenName"] + " #" + transactions["tokenID"])
        if transactions["contractAddress"] not in collection_stats:
            # get_collection_stats handles missing slugs
            collection_stats["contractAddress"] = get_collection_stats(
                transactions["openseaSlug"]
            )
            nfts[unique_id] = {
                **transactions,
                **collection_stats["contractAddress"],
            }

        response = requests.get(
            NFT_PORT_API_URL + "/transactions/nfts/" + unique_id,
            params={"chain": "ethereum", "type": ["transfer", "sale"]},
            headers=NFT_PORT_HEADERS,
        )
        data = response.json()
        nft_transactions = list(filter(filter_junk_sales, data["transactions"]))

        if thief_wallet is not None:
            thief = thief_wallet
        else:
            thief = transactions["theft"]["to"]
        # Find details about what thief did with the NFT
        nfts[unique_id] = {
            **nfts[unique_id],
            **find_thief_activity(nft_transactions, transactions, thief),
        }

        # Try to find information about how the victim acquired the NFT
        victim = None
        if victim_wallet is not None:
            victim = victim_wallet
        elif "theft" in transactions:
            victim = transactions["theft"]["from"]
        if victim is not None:
            sale = find_by(nft_transactions, type="sale", buyer_address=victim)
            if sale:
                nfts[unique_id]["victim_purchase"] = sale

    with open("price_data.json", "w+") as json_file:
        json.dump(nfts, json_file, indent=2)
    return nfts
