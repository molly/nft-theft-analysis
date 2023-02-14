import requests
from constants import SHARED_HEADERS
from secrets import OPENSEA_API_KEY
from time import sleep
from utils import pick

API_URL = "https://api.opensea.io/api/v1"
HEADERS = {**SHARED_HEADERS, "Accept": "application/json", "X-API-KEY": OPENSEA_API_KEY}
COLLECTION_STATS_KEYS = [
    "one_day_average_price",
    "one_day_sales",
    "seven_day_sales",
    "seven_day_average_price",
    "thirty_day_sales",
    "thirty_day_average_price",
    "floor_price",
    "average_price",
]


def request_with_backoff(*args, **kwargs):
    response = requests.get(*args, **kwargs)
    if response.status_code == 200:
        return response
    elif response.status_code == 429:
        print(
            "Throttled, trying again in " + sleep(response.headers["retry-after"]) + "s"
        )
        sleep(response.headers["retry-after"])
        return request_with_backoff(*args, **kwargs)
    else:
        raise Exception


def get_slug(contract):
    print("Getting slug for " + contract)
    response = request_with_backoff(
        API_URL + "/asset_contract/" + contract, headers=HEADERS
    )
    data = response.json()
    if "collection" in data:
        return data["collection"]["slug"]
    if "success" in data:
        # Collection not found on OpenSea
        return None
    else:
        raise Exception


def get_collection_stats(slug):
    if not slug:
        return dict((k, None) for k in COLLECTION_STATS_KEYS)
    response = request_with_backoff(API_URL + "/collection/" + slug + "/stats")
    data = response.json()
    return pick(data["stats"], COLLECTION_STATS_KEYS)
