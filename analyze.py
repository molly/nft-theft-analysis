import argparse
import json
import os
from etherscan import get_transfers
from opensea import get_slug
from price import get_price_details_for_transactions
from report import make_report
from utils import *


def sort_by_nft(transactions, thief_wallet=None, victim_wallet=None, **kwargs):
    nfts = {}
    slugs = {}
    for transaction in transactions:
        unique_id = transaction["contractAddress"] + "/" + transaction["tokenID"]
        if unique_id not in nfts:
            # Store some common data at the root level for easy retrieval/filtering later
            nfts[unique_id] = {
                "contractAddress": transaction["contractAddress"],
                "tokenName": transaction["tokenName"],
                "tokenID": transaction["tokenID"],
                "tokenSymbol": transaction["tokenSymbol"],
            }

        if transaction["contractAddress"] not in slugs:
            slugs[transaction["contractAddress"]] = get_slug(
                transaction["contractAddress"]
            )
        nfts[unique_id]["openseaSlug"] = slugs[transaction["contractAddress"]]

        if not victim_wallet:
            if address_equals(transaction["to"], thief_wallet):
                nfts[unique_id]["theft"] = transaction
            elif address_equals(transaction["from"], thief_wallet):
                nfts[unique_id]["transfer"] = transaction
            else:
                # Shouldn't happen since we queried for only transactions to/from this address
                raise Exception
        else:
            nfts[unique_id]["theft"] = transaction
    return nfts


def analyze(args):
    if args.dev and os.path.exists("price_data.json"):
        with open("price_data.json", "r") as price_json_file:
            details = json.load(price_json_file)
    elif args.dev and os.path.exists("nft_data.json"):
        with open("nft_data.json", "r") as nft_json_file:
            details = json.load(nft_json_file)
    else:
        transactions = get_transfers(**vars(args))
        nfts = sort_by_nft(transactions, **vars(args))
        with open("nft_data.json", "w+") as json_file:
            json.dump(nfts, json_file, indent=2)
        details = get_price_details_for_transactions(nfts, **vars(args))

    make_report(details)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze an incident of NFT theft.")
    wallet_group = parser.add_mutually_exclusive_group(required=True)
    wallet_group.add_argument("-thief", dest="thief_wallet", action="store")
    wallet_group.add_argument("-victim", dest="victim_wallet", action="store")
    parser.add_argument(
        "-start", dest="start_timestamp", action="store", type=valid_date
    )
    parser.add_argument("-end", dest="end_timestamp", action="store", type=valid_date)
    parser.add_argument("--dev", dest="dev", action="store_true")

    parser_args = parser.parse_args()
    analyze(parser_args)
