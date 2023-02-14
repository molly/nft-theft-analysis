from opensea import get_collection_stats
import json

API_URL = "https://api.etherscan.io/api"


def get_price_details_for_transactions(nfts_original):
    nfts = nfts_original.copy()
    collection_stats = {}
    try:
        for unique_id, transactions in nfts.items():
            print(
                "Tracing: " + transactions["tokenName"] + " #" + transactions["tokenID"]
            )
            if transactions["contractAddress"] not in collection_stats:
                # get_collection_stats handles missing slugs
                collection_stats["contractAddress"] = get_collection_stats(
                    transactions["openseaSlug"]
                )
                nfts[unique_id] = {
                    **transactions,
                    **collection_stats["contractAddress"],
                }

    except Exception as e:
        print(e)
    finally:
        with open("price_tmp.json", "w+") as json_file:
            json.dump(nfts, json_file, indent=2)
        return nfts
