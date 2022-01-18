from apiconnect import getTicker
import matplotlib.pyplot as plt
from numpy import diff

averagelen = 0

def getDelta(ticker, period, start, end):
    global averagelen
    data = getTicker(ticker, period, start, end)
    vwap = [i for i in data["vwap"]]
    vwapRange = len(vwap)

    averagelen+=vwapRange
    rightRanges = []
    leftRanges = []
    openprices = [i for i in data["open"]]
    for i in range(1, vwapRange):
        rightRanges.append(sum(vwap[:i]) / (i))

    for i in range(vwapRange - 1):
        leftRanges.append(sum(vwap[i:]) / ((vwapRange - i)))
    closed = [(i + j) / 2 for i, j in zip(leftRanges, rightRanges)]
    ranges = [i for i in range(vwapRange - 1)]
    leftRangeDeltaValues = [i - j for i, j in zip(closed, leftRanges)]
    rightRangeDeltaValues = [i - j for i, j in zip(rightRanges, closed)]
    closedDeltaValues = [
        (i + j) / 2 for i, j in zip(rightRangeDeltaValues, leftRangeDeltaValues)
    ]
    delta = sum(closedDeltaValues) / len(closedDeltaValues)
    print(f"{ticker}:{delta}")
    plt.plot(closedDeltaValues)


tickers = [
    "CSPR",
    "RSI",
    "COUR",
    "TALS",
    "MEDP",
    "AFRM",
    "HUDI",
    "TXG",
]

for ticker in tickers:
    getDelta(ticker, 1, "2021-12-08", "2022-01-18T14:51:21+00:00")


plt.plot([0 for i in range(int(averagelen/len(tickers)))])

plt.show()
