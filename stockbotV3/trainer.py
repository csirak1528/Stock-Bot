from numpy.core import machar
import neuralnet
import stockbotV3
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from numba import njit

cache = stockbotV3.parse_cache()
reach = 20


def get_ticker_data():
    fail = []
    for ticker in stockbotV3.tickers:
        data = cache["trained"]
        try:
            data[ticker["ticker"]]
        except:
            fail.append(ticker["ticker"])
    return get_training_data(fail)


def get_training_data(tickers):
    raw = []
    start = reach
    breakpoint = 2
    limit = 2
    profit = .5
    curdata = yf.download(tickers=tickers, period='1d',
                          interval='1m', progress=False)
    for minute in curdata["Open"]:
        raw.append(minute)
    mn = min(raw)

    prices = [i-mn for i in raw]
    res = []
    """
    Runs through all the minues and collects start amount of minutes beforehand
    and then goes into the future start/breakpoint number of times to look at the possible profit
    """
    for i, price in enumerate(prices):
        if i > start and len(prices) > int(i+start/breakpoint):
            nums = []
            for j in range(i-start, i):
                nums.append(prices[j])
            decision = 0
            bought = 0
            boughtprice = -1
            for k in range(i, int(i+start/breakpoint)):
                if prices[k] > price+profit:
                    decision += 1
                    boughtprice = price

                if prices[k]+profit > boughtprice and decision:
                    decision -= 1

            nums.append(price)
            if decision > limit:
                res.append([nums, 1])
            elif decision < -1*limit:
                res.append([nums, -1])
            else:
                res.append([nums, 0])
    return res


if __name__ == '__main__':
    data = get_ticker_data()
    brain = neuralnet.NeuralNetwork([reach+1, 21, 21, 10, 1])
    test = data[int(len(data)/2):]
    train = data[:int(len(data)/2)]
    X = np.array([i[0] for i in train])
    y = np.array([i[1] for i in train])
    brain.fit(X, y)
    p = []
    d = []
    for i in test:
        p.append([i[0][-1]])
    t = np.array([i[0] for i in test])
    for e in t:
        d.append(brain.predict(e))
    for i, val in enumerate(p):
        print(d[i][0][0])
        if round(d[i][0][0]) == 1:
            plt.plot([i], val, "g^")
        if round(d[i][0][0]) == -1:
            plt.plot([i], val, "rv")

    plt.plot([i for i in range(len(p))], p)
    plt.pause(.1)
    plt.show()
