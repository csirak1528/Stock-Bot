from numpy.core import machar
import neuralnet
import stockbotV3
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import json

cache = stockbotV3.parse_cache()
reach = 20


def get_ticker_data():
    fail = []
    for ticker in stockbotV3.tickers:
        data = cache
        try:
            data[ticker["ticker"]]
        except:
            fail.append(ticker["ticker"])
    return get_training_data(fail)


def get_training_data(tickers):
    for ticker in tickers:
        raw = []
        start = reach
        breakpoint = 2
        limit = 2
        profit = .01
        curdata = yf.download(tickers=ticker,period="5d", interval="1m",progress=False)
        for minute in curdata["Open"]:
            raw.append(minute)
        mn = min(raw)
        mx = max(raw)
        prices = [(i-mn)/(mx-mn) for i in raw]
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
                for k in range(i, int(i+start/breakpoint)):
                    if prices[k] > price+profit:
                        decision += 1
                    if prices[k]+profit < price:
                        decision -= 1

                nums.append(price)
                if decision > limit:
                    res.append([nums, 1])
                elif decision < -1*limit:
                    res.append([nums, -1])
                else:
                    res.append([nums, 0])
            cache[ticker] = res
        p = []
        d = []
        for i in res:
            p.append([i[0][-1]])
            d.append(i[1])
        plt.plot([i for i in range(len(p))],p)
        for i in range(len(d)):
            if d[i] == 1:
                plt.plot(i,p[i], "g^")
            if d[i] == -1:
                plt.plot(i,p[i],"rv")
    with open('stockbotV3/cached_data.json',"w") as json_file:
        json.dump(cache,json_file)


if __name__ == '__main__':
    get_ticker_data()
    cur=cache["GOOG"]
    nums=[]
    res = []
    for i in cur:
        nums.append(i[0])
        if i[1] == 1:
            res.append(1)
        else:
            res.append(0)

    X = np.array(nums)
    y =np.array(res)
    buy = neuralnet.NeuralNetwork([reach+1,20,1],activation="tanh")
    buy.fit(X,y)
    for num , pred in zip(X, res):
        print(pred, buy.predict(num)[0][0])
    plt.show()


    