import requests
from secrets import OPENSEA_API_KEY
from utils import address_equals

API_URL = "https://api.opensea.io/api/v1"
HEADERS = {"Accept": "application/json", "X-API-KEY": OPENSEA_API_KEY}


def is_theft(event, thief_wallet=None, victim_wallet=None):
    """A theft is either where an NFT was transferred TO a thief wallet or AWAY FROM a victim wallet"""
    return (
        thief_wallet is not None
        and address_equals(event["to_account"]["address"], thief_wallet)
    ) or (
        victim_wallet is not None
        and address_equals(event["from_account"]["address"], victim_wallet)
    )


def get_transfers(
    thief_wallet=None, victim_wallet=None, start_timestamp=None, end_timestamp=None
):
    results = []
    query = {"account_address": thief_wallet or victim_wallet, "cursor": None}
    if start_timestamp:
        query["occurred_after"] = start_timestamp.timestamp() - 1
    if end_timestamp:
        query["occurred_before"] = end_timestamp.timestamp() + 1

    while True:
        response = requests.get(API_URL + "/events", params=query, headers=HEADERS)
        data = response.json()
        for event in data["asset_events"]:
            if is_theft(event, thief_wallet, victim_wallet):
                # Filter transactions that don't appear to be thefts
                results.append(event)
        query["cursor"] = data["next"]
        if query["cursor"] is None:
            break
    print(len(results))
    return results
