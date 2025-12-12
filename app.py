import yaml
import yfinance as yf
import time
import os

# Loads up configs on start
with open("holdings.yaml") as f:
    config = yaml.safe_load(f)

# Gets listed tickers from holdings.yaml
def load_holdings():
    with open("holdings.yaml", "r") as f:
        data = yaml.safe_load(f)
        return data["tickers"]

# Pulls stock price for each ticker
def get_prices(tickers):
    data = yf.download(tickers, period="1d", interval="1m", progress=False, auto_adjust=True)
    return data["Close"].iloc[-1].to_dict()

# Function to print values, will be updated to "update"
def print_total():
    # Gets all of the holdings from the YAML in a variable
    holdings = load_holdings()

    # Pulls the tickers from said YAML
    tickers = list(holdings.keys())

    # Gets the price/share for the given ticker
    prices = get_prices(tickers)

    # Sets total variable
    total = 0

    # Sets up breakdown list for use in print loop
    breakdown = []

    # Loops through each ticker pulling price and number of shares
    for ticker, shares in holdings.items():
        price = prices[ticker]
        value = price * shares
        
        # Adds value of said ticker to total
        total += value

        # Appends to breakdown list for easy use later
        breakdown.append((ticker, shares, price, value))

    # Clears terminal (Can delete later)
    os.system("cls" if os.name == "nt" else "clear")

    # Prints header
    print("=$=$= Porfolio Total =$=$=")

    # Prints current total
    print(f"Total Value: ${total:,.2f}")

    # Loops through tickers' data and prints them in an easily readable way
    for ticker, shares, price, value in breakdown:
        print(f"{ticker}: {shares} x {price:.2f} = ${value:,.2f}")

# Main Run Loop
def main():
    while True:
        try:
            print_total()
            time.sleep(config["update_time"])
        except KeyboardInterrupt:
            print("\nQuitting HexenFolio")
            break

if __name__ == "__main__":
    main()