import yfinance as yf
from time import sleep 
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from tqdm import tqdm
import sys
import matplotlib.pyplot as plt

"""
api-key:
account:
"""

counter=0
intreval=1
start_time=datetime.datetime.now()
money_list=[1]
info={}
watchlist=['MSFT', 'AMZN','TSLA','PLTR','AAPL','TWTR',"GOOG",
            "NFLX","VZ","BABA","NKLA","BA","CSCO","UBER","FB","LYFT",
            "GS","IBM","NVDA","MU"]
    

def get_cur_price(companies,info):
    global intreval
    stock_data={}
    for company in companies:
        try:
            data= yf.download(tickers=company, period='2h',interval='1m',progress=False)
        except (IndexError,KeyError):
            continue
        prices=data['Open']
        spacer=15
        try:
            stock_data[company] = prices[(intreval-1)*spacer: intreval*spacer]
        except IndexError:
            print('fd')
            stock_data[company] = prices[(intreval-1)*spacer: len(prices)-1]
    intreval+=1
    return stock_data

def convert(sec): 
    min_, sec_ = divmod(sec, 60) 
    hour, min_ = divmod(min_, 60) 
    return "%d:%02d:%02d" % (hour, min_, sec) 

# sender email address
def update_user(out,money,end,percent):
    email_user = 'calebsirak@gmail.com'
    email_password = 'fireredleaf'
    email_send = ['calebsirak@gmail.com']
    subject = f'Stock Closing Value: {money}'
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['Subject'] = subject 
    body = "\n".join(out) + "\n"+ end+f"\nPercent Change: {percent}%"
    msg.attach(MIMEText(body,'plain'))
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)
    server.sendmail(email_user,email_send,text)
    server.quit()


def sell_mode(bought, info, end=""):
    global start_money
    global money
    global max_sell
    global prev_cost
    out=[]
    buffer=0
    watchers=[i[0] for i in bought]
    while len(bought)>0:
        try:
            stock_prices=get_cur_price(watchers,info)
            
            for company in stock_prices.items():
                name=company[0]
                stock_data=company[1]
                try:
                        cur_price=stock_data[len(stock_data)-1]
                        prev_cost[name]=cur_price
                        stock_data=(stock_data[1:],stock_data)[len(stock_data)%2==0]
                        cur_price=stock_data[len(stock_data)-1]
                except IndexError:
                        cur_price= prev_cost[name]
                
                for pos,stock in enumerate(bought):
                    if name in stock:
                        if cur_price - stock[1] >.1:
                            money+=cur_price
                            out.append(f"Sell:{name} ${cur_price-stock[1]}")
                            bought.pop(pos)

            buffer+=1
            if buffer>=30:
                raise KeyboardInterrupt()
        except (KeyboardInterrupt, IndexError):
            for stock in bought:
                money+=stock[1]
                out.append(f"{stock[0]}: {stock[1]}")
        break
    percent=100*((money/max_sell)-1)
    print(f"\nQuick Sell ${money}, Rate: {percent}%")
    update_user(out,money,end,percent)
    max_sell=money
    money=max_sell


start_money=10000
max_sell=start_money
money=start_money
prev_cost={}
while True:
    money=max_sell
    bought = []
    watch={}
    start =datetime.datetime.now().minute
    time=start
    total_profit=0
    sell=[]
    buy=[]
    stocks=[]
    blocked=[]
    cur_sold=[]
    cash_low=5
    total_value=0
    oldval=0
    try:
        while True:
            try:
                stock_prices=get_cur_price(watchlist,info)
                #gets stock data from yfinance and adds it to hashtables for further data analysis
                for company in stock_prices.items():
                    name=company[0]
                    stock_data=company[1]
                    cur_price=stock_data[len(stock_data)-1]
                    prev_cost[name]=cur_price
                    stock_data=(stock_data[1:],stock_data)[len(stock_data)%2==0]
                    data_len= len(stock_data)-1
                    split_len=2
                    slopes=[]

                    for i in range(data_len):
                        cur_slope=1000*(stock_data[i+1] - stock_data[i])/stock_data[i]
                        slopes.append(cur_slope)
                    if len(slopes)>0:
                        avg_slope=sum(slopes)/len(slopes)
                    else:
                        avg_slope=0
                    if name in watch.keys():
                        watch[name]=avg_slope
                        if avg_slope< .5 and avg_slope > -.1 and money - cur_price >0:
                            money-=cur_price
                            buy.append(f"Bought: {name} ${cur_price}")
                            bought.append([name,cur_price])
                            blocked.append(name)
                    for pos,stock in enumerate(bought):
                        if stock[0] ==name:
                            stocks.append([name,cur_price])
                        if stock[0] ==name and name not in blocked:
                            if not watch.get(name) == None:
                                print(avg_slope-watch[name])
                            if (avg_slope-watch[name]>.2 or cur_price-stock[1]>cash_low):
                                profit=cur_price-stock[1]
                                money+=cur_price
                                total_profit+=profit
                                sell.append(f"Sell: {name} P>{profit}")
                                cur_sold.append([name,stock[1]])
                                del bought[pos]
                                
                """if total_value-max_sell>20:
                    print("max")
                    for pos, stock in enumerate(bought):
                        if name == stock[0]:
                            if cur_price-stock[1]>3:
                                money+= cur_price
                                sell.append(f"Sell: {name} P>{cur_price-stock[1]}")
                                bought.pop(pos)
                    break"""
                    
                    
                if avg_slope < .3 and avg_slope > -.1:
                        watch[name] = avg_slope
                print("\n$",money,"\n")
                for i in watch.items():
                    print(f"{i[0]}: {i[1]}")
                hour=datetime.datetime.now().hour
                mins=datetime.datetime.now().minute
                sec=datetime.datetime.now().second
                if sec<10:
                    sec=f"0{sec}"
                if mins<10:
                    mins=f"0{mins}"
                if hour>12:
                    hour=f"{hour-12}"
                print(f"{hour}:{mins}:{sec}")
                s="\n".join(sell)
                k={}
                for i in bought:
                    if k.get(i[0])==None:
                        k[i[0]]=i[1]
                    else:
                        k[i[0]]=k[i[0]]+i[1]
                b="\n".join([f"{i[0]}: ${i[1]}" for i in k.items()])
                total_value=0
                for i in stocks:
                    total_value+=i[1]
                for i in cur_sold:
                    total_value-=i[1]
                total_value=total_value+money
                out=f"Total Value: {total_value}\n\n{b}\n\n{s}"
                print(out)
                try:
                    print(f"Change {100*((total_value-oldval)/oldval)}%")
                except ZeroDivisionError:
                    pass
                oldval=total_value
                sell=[]
                stocks=[]
                blocked=[]
                cur_sold=[]
                money_list.append(total_value)
                plt.plot([i for i in range(len(money_list))],money_list)
                plt.axis([0,800,9800,10500])
                plt.pause(0.05)

                while not start==time-1:
                    time =datetime.datetime.now().minute
                start=time
                counter+=1
            except (KeyboardInterrupt,ConnectionError,ConnectionAbortedError,ConnectionRefusedError):
                print("\nBeginning Shut down")
                counter+=1
                print(f"Total Runtime:{counter} minutes")
                end=datetime.datetime.now()
                time=end-start_time
                k=time.total_seconds()
                end_out=f"Total Runtime:{convert(k)}"
                sell_mode(bought,info,end_out)
                break

    except KeyboardInterrupt:
        print("$",money)
        print("%",100*(money-start_money)/start_money)
        e = sys.exc_info()
        break
plt.show()
end=datetime.datetime.now()
time=end-start_time
print(f"Total Runtime:{counter} minutes")

#print(f"Total Runtime:{convert(time.total_seconds())}")
