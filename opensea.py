import requests
from secrets import OPENSEA_API_KEY

API_URL = "https://api.opensea.io/api/v1"
HEADERS = {"Accept": "application/json", "X-API-KEY": OPENSEA_API_KEY}


def get_transfers(
    thief_wallet=None, victim_wallet=None, start_timestamp=None, end_timestamp=None
):
    results = []
    query = {"account_address": thief_wallet or victim_wallet, "next": None}
    if start_timestamp:
        query["occurred_after"] = start_timestamp.timestamp() - 1
    if end_timestamp:
        query["occurred_before"] = end_timestamp.timestamp() + 1

    response = requests.get(API_URL + "/events", params=query, headers=HEADERS)
    data = response.json()
    results.extend(data["asset_events"])
    query["next"] = data["next"]
    while query["next"]:
        response = requests.get(API_URL + "/events", params=query, headers=HEADERS)
        data = response.json()
        results.append(data["asset_events"])
        query["next"] = data["next"]

    return results
