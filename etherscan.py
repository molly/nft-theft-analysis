import requests
from secrets import ETHERSCAN_API_KEY
from utils import *

API_URL = "https://api.etherscan.io/api"


def get_block_numbers(start_timestamp=None, end_timestamp=None):
    results = {"start": None, "end": None}
    params = {
        "module": "block",
        "action": "getblocknobytime",
        "apikey": ETHERSCAN_API_KEY,
    }
    if start_timestamp:
        response = requests.get(
            API_URL,
            params={
                **params,
                "timestamp": int(start_timestamp.timestamp()),
                "closest": "before",
            },
        )
        data = response.json()
        if data["status"] == "1":
            results["start"] = data["result"]
    if end_timestamp:
        response = requests.get(
            API_URL,
            params={
                **params,
                "timestamp": int(end_timestamp.timestamp()),
                "closest": "after",
            },
        )
        data = response.json()
        if data["status"] == "1":
            results["end"] = data["result"]
    return results


def make_transaction_filter(thief_wallet=None, victim_wallet=None):
    def transaction_filter(transaction):
        return (
            thief_wallet is None or address_equals(transaction["to"], thief_wallet)
        ) and (
            victim_wallet is None or address_equals(transaction["from"], victim_wallet)
        )

    return transaction_filter


def get_transfers(
    thief_wallet=None, victim_wallet=None, start_timestamp=None, end_timestamp=None
):
    blocks = None
    if start_timestamp or end_timestamp:
        blocks = get_block_numbers(start_timestamp, end_timestamp)
        print(blocks)

    response = requests.get(
        API_URL,
        {
            "module": "account",
            "action": "tokennfttx",
            "address": thief_wallet or victim_wallet,
            "startblock": blocks and blocks["start"],
            "endblock": blocks and blocks["end"],
            "sort": "asc",
            "apikey": ETHERSCAN_API_KEY,
        },
    )
    data = response.json()
    data = list(
        filter(make_transaction_filter(thief_wallet, victim_wallet), data["result"])
    )
    return data
