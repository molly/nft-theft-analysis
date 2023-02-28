import csv
from etherscan import get_current_eth_price


def get_best_price_average(nft, eth_price):
    if nft["one_day_sales"] > 25:
        return [
            nft["one_day_average_price"] * eth_price,
            "{:0.0f}/1D".format(nft["one_day_sales"]),
        ]
    elif nft["seven_day_sales"] > 25:
        return [
            nft["seven_day_average_price"] * eth_price,
            "{:0.0f}/7D".format(nft["seven_day_sales"]),
        ]
    elif nft["thirty_day_sales"] > 25:
        return [
            nft["thirty_day_average_price"] * eth_price,
            "{:0.0f}/30D".format(nft["thirty_day_sales"]),
        ]
    else:
        return [nft["average_price"], "{:0.0f}/all".format(nft["total_sales"])]


def make_report(nfts):
    with open("out.tsv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter="\t")

        # Write header row
        csvwriter.writerow(
            [
                "Contract/ID",
                "Token name",
                "ID",
                "Floor USD",
                "Average price USD",
                "Average price period",
                "Victim purchase amount USD",
                "Thief sale amount USD",
                "Post-theft sale amount USD",
                "Resale price or floor",
                "Victim purchase timestamp",
                "Sale timestamp",
            ]
        )

        eth_price = get_current_eth_price()
        for unique_id, nft in nfts.items():
            theft_key = "thief_sale" if "thief_sale" in nft else "sale_after_theft"
            floor_usd = nft["floor_price"] * eth_price if nft["floor_price"] else ""
            average_price = get_best_price_average(nft, eth_price)
            victim_purchase_price = (
                nft.get("victim_purchase", {})
                .get("price_details", {})
                .get("price_usd", "")
            )
            thief_resale_price = (
                nft.get("victim_purchase", {})
                .get("price_details", {})
                .get("price_usd", "")
            )
            sale_after_theft_price = (
                nft.get("victim_purchase", {})
                .get("price_details", {})
                .get("price_usd", "")
            )
            csvwriter.writerow(
                [
                    unique_id,
                    nft["tokenName"],
                    nft["tokenID"],
                    floor_usd,
                    average_price[0],
                    average_price[1],
                    victim_purchase_price,
                    thief_resale_price,
                    sale_after_theft_price,
                    thief_resale_price or sale_after_theft_price or floor_usd,
                    nft.get("victim_purchase", {}).get("transaction_date", ""),
                    nft.get(theft_key, {}).get("transaction_date", ""),
                ]
            )
