import yaml

# This is a bunch of duct taped together unused junk code for the time being, please don't read this lol

FILE = "holdings.yaml"

def load_holdings():
    with open(FILE, "r") as f:
        return yaml.safe_load(f)

def save_holdings(data):
    with open(FILE, "w") as f:
        yaml.save_dump(data, f, sort_keys=False)

# Add a ticker to the holdings list
def add_ticker(ticker, shares):
    data = load_holdings(ticker, shares)
    data = load_holdings()
    data["tickers"][tickers] += shares
    save_holdings()

# Remove a ticker from the holdings list
def remove_ticker(ticker):
    data = load_holdings()
    if ticker in data["tickers"]:
        del data["tickers"][ticker]
    else:
        print("Ticker ", ticker, "not found. Please Try again")
    save_holdings()

# Set the value of a ticker from the list
def set_ticker_value(ticker, value):
    data = load_holdings()
    if ticker in data["tickers"]:
        data["tickers"][ticker] = value
        print("Added ", ticker, " with ", value, " shares")
    else:
        print(ticker, " Not found. Please try again.")