from etherscan_scraper import get_transaction_details
import json

API_URL = "https://api.etherscan.io/api"


def get_price_details_for_transactions(transactions):
    try:
        for tx in transactions:
            print("Tracing: " + tx["tokenName"] + " #" + tx["tokenID"])
            tx["details"] = get_transaction_details(tx["hash"])
    except Exception as e:
        print(e)
    finally:
        with open("tmp.json", "w+") as json_file:
            json.dump(transactions, json_file, indent=2)
