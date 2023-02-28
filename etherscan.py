import requests
from constants import SHARED_HEADERS
from secrets import ETHERSCAN_API_KEY
from utils import address_equals

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
            headers=SHARED_HEADERS,
        )
        data = response.json()
        if data["status"] == "1":
            results["end"] = data["result"]
    return results


def get_transfers(
    thief_wallet=None,
    victim_wallet=None,
    start_timestamp=None,
    end_timestamp=None,
    **kwargs
):

    blocks = None
    if start_timestamp or end_timestamp:
        blocks = get_block_numbers(start_timestamp, end_timestamp)

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
        headers=SHARED_HEADERS,
    )
    data = response.json()
    data = list(data["result"])
    if victim_wallet is not None:
        # Don't need transactions TO the victim
        data = filter(lambda trans: address_equals(trans["from"], victim_wallet), data)
    return data


def get_current_eth_price():
    response = requests.get(
        API_URL,
        {"module": "stats", "action": "ethprice", "apikey": ETHERSCAN_API_KEY},
        headers=SHARED_HEADERS,
    )
    data = response.json()
    return float(data["result"]["ethusd"])
