import yfinance as yf

def get_price(company):
    data=yf.download(tickers=company, period='2h',interval='1m',progress=False)
    data=data['Open']
    data=data[len(data)-15:]
    return data

watchlist=[]
bought=[]
watching={}
while True:
    for stock in watchlist:
        prices=get_price(stock)
        cur_price=prices[-1]
        start_price=prices[0]
        slopes=[]
        for i in range(len(prices)):
            slopes.append((prices[i+1]-prices[i])/start_price)
        slope=sum(slopes)/len(slopes)
        print(slope)
