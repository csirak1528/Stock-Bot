import cryptocompare


class Entity:
    def __init__(self, ticker, ent_type, get_method="default", currency="USD"):
        self.ticker = ticker
        self.ent_type = ent_type
        self.get_method = get_method
        self.bought_price = -1
        self.prices = [self.price]
        self.currency = currency
        self.get_history()

    def get(self):
        if self.getMethod == "default":
            if self.ent_type == "crypto":
                self.prices.append(
                    cryptocompare.get_price(self.tag, self.currency))

    def decision(self):
        self.get()
        print(self.prices)

    def parse_prices(self):
        pass

    def get_history(self):
        pass

    def __str__(self):
        print(f"{self.bought_price} -> {self.prices[-1]}")
