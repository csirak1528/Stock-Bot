import yfinance as yf
import pickle
import datetime
import time

try:
    with open("money.pk","rb") as money_data:
        money = pickle.load(money_data)
except (FileNotFoundError, EOFError):
    print("BUGGGGGGG")
    money=10000

def get_price(company):
    data=yf.download(tickers=company, period='2h',interval='1m',progress=False)
    data=data['Open']
    data=data[len(data)-15:]
    return data
def convert(sec): 
    min_, sec_ = divmod(sec, 60) 
    hour, min_ = divmod(min_, 60) 
    return "%d:%02d:%02d" % (hour, min_, sec) 

watchlist=['MSFT', 'AMZN','TSLA','PLTR','AAPL','TWTR',"GOOG","NFLX","VZ","BABA","NKLA","BA","CSCO","UBER","FB","LYFT",
            "GS","IBM","NVDA","MU"]
bought=[]
watching={}
money=10000
start_time=datetime.datetime.now()

while True:
    start=datetime.datetime.now().minute
    try:    
        blocked=[]
        sold=[]
        watching={}
        cur_prices={}
        for stock in watchlist:
            prices=get_price(stock)
            cur_price=prices[-1]
            cur_prices[stock]=cur_price
            start_price=prices[0]
            slopes=[]
            for i in range(len(prices)-1):
                slopes.append(1000*(prices[i+1]-prices[i])/start_price)
            slope=sum(slopes)/len(slopes)
            watching[stock]=slope
            if slope>.1 and slope<.4 and money-cur_price>0:
                bought.append([stock,cur_price])
                money-=cur_price
                blocked.append([stock,cur_price])
        total_value=0
        total_value+=money
        for pos,stock in enumerate(bought):
            total_value+=cur_prices[stock[0]]
            if stock not in blocked:
                name=stock[0]
                bought_price=stock[1]
                cur_price=cur_prices[name]
                slope=watching[name]
                if cur_price-bought_price>0:
                    bought.pop(pos)
                    money+=cur_price
                    sold.append((f"{name}: P>{cur_price-bought_price}"))
    
        
        print("\n\nBuying Power",money)
        print("Total value",total_value)
        print("\n\nWatching:")
        for (i,j) in watching.items():
            print(f"{i}:{j}") 
        print("\n\nSold:")
        for i in sold:
            print(i)
        print("\n\nBought:")
        for i in blocked:
            print(f"Buy: {i[0]}: ${i[1]}")
        now=datetime.datetime.now().minute
        while start==now:
            now=datetime.datetime.now().minute
    except KeyboardInterrupt:
        try:
            while len(bought)>0:
                for i in bought:
                    name=stock[0]
                    bought_price=stock[1]
                    cur_price=get_price(stock[0])[-1]
                    if cur_price-bought_price>0:
                        bought.pop(pos)
                        money+=cur_price
                        sold.append((f"{name}: P>{cur_price-bought_price}"))
                for i in sold:
                    print(sold)
        except KeyboardInterrupt:
            print("Quick")
            for i in bought:
                name=stock[0]
                bought_price=stock[1]
                cur_price=get_price(stock[0])[-1]
                money+=cur_price
                
        break
with open("money.pk","wb") as money_data:
       pickle.dump(money,money_data)   
end_time=datetime.datetime.now()-start_time
print(f"Total Runtime:{convert(end_time.total_seconds())}",f" ${money}")
 