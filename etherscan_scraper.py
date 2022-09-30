from bs4 import BeautifulSoup
from selenium import webdriver
import re


def get_transaction_details(txhash):
    try:
        wd_options = webdriver.ChromeOptions()
        wd_options.add_argument = "--headless"
        browser = webdriver.Chrome(
            options=wd_options, executable_path="/Users/molly/Programming/chromedriver"
        )
        browser.get("https://etherscan.io/tx/" + txhash)
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")
        transfer_row_headers = soup.find_all(text=re.compile("Tokens Transferred: ?"))
        transfer_rows = []
        for header in transfer_row_headers:
            for parent in header.parents:
                if parent.name == "div" and "row" in parent["class"]:
                    transfer_rows.append(parent)

        transfers_text = []
        for row in transfer_rows:
            for entry in row.find_all("li"):
                transfers_text.append(list(entry.stripped_strings))

        transfers = []
        for entry in transfers_text:
            transfer = {
                "from": entry[1],
                "to": entry[3],
                "token": re.sub("[()]", "", entry[8]),
            }
            if entry[5].replace(".", "", 1).isdigit():
                transfer["amount"] = float(entry[5])

            transfers.append(transfer)
        return transfers
    except Exception as e:
        print(txhash)
