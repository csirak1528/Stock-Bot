import stock
import json

tickers = [{
    "ticker": "GOOG",
    "type": "stock"
},
    # {
    # "ticker": "TSLA",
    # "type": "stock", },
    # {
    # "ticker": "BTC-USD",
    # "type": "stock"},
    #  {
    # "ticker": "ETC-USD",
    # "type": "stock"}
]

bought = []
sold = []


def parse_cache():
    with open('stockbotV3/cached_data.json') as json_file:
        data = json.load(json_file)
        return data


def start():
    for i in tickers:
        pass


if __name__ == "__main__":
    start()
