import stock
from keys import keys

tickers = []

def getKeys():
    global key
    global secret
    key = keys["key"]
    secret = keys["secret"]

def start():
    getKeys()

if __name__ == "__main__":
    start()


