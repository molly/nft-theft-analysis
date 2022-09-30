import argparse
from etherscan import get_transfers
from price import get_price_details_for_transactions
from utils import *
from etherscan_scraper import get_transaction_details


def analyze(args):
    transactions = get_transfers(**vars(args))
    price_details = get_price_details_for_transactions(transactions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze an incident of NFT theft.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-thief", dest="thief_wallet", action="store")
    group.add_argument("-victim", dest="victim_wallet", action="store")
    parser.add_argument(
        "-start", dest="start_timestamp", action="store", type=valid_date
    )
    parser.add_argument("-end", dest="end_timestamp", action="store", type=valid_date)
    # TODO: Multiple thief/victim wallets, list of NFTs

    parser_args = parser.parse_args()
    resp = analyze(parser_args)
