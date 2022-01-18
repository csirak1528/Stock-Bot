from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
import pandas as pd
import config

import matplotlib.pyplot as plt

api = REST(config.APCA_API_KEY_ID, config.APCA_API_SECRET_KEY, config.APCA_API_BASE_URL)


def getTicker(ticker, hourRepeat, start, end, to_csv=False):
    data = api.get_bars(
        ticker, TimeFrame(hourRepeat, TimeFrameUnit.Day), start, end, adjustment="raw"
    ).df
    if to_csv:
        data.to_csv("./main.csv")
    return data
