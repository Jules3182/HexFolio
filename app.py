import yaml
import yfinance as yf
import time

# Utils split into other file for future use
from holdings_utils import add_ticker, remove_ticker, set_ticker_value

# Terminal management stuff moved to other file
from tui import print_total

# Loads up user config on start
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Gets listed tickers from holdings.yaml
def load_holdings():
    with open("holdings.yaml", "r") as f:
        data = yaml.safe_load(f)
        return data["tickers"]

# Get opening prices for each ticker
def get_opening_prices(tickers):
    opening_prices = {}

    # Loop pulling opening prices for each ticker
    for ticker in tickers:
        hist = yf.Ticker(ticker).history(period="1d", interval="1m")

        # Case for empty opening value
        if hist.empty:
            opens[ticker] = None
            continue

        # Gets most recent opening price
        open_price = hist.iloc[0]["Open"]
        opening_prices[ticker] = float(open_price)

    return opening_prices

# Pulls stock price for each ticker
def get_current_prices(tickers):
    data = yf.download(tickers, period="1d", interval="1m", progress=False, auto_adjust=True)
    return data["Close"].iloc[-1].to_dict()

# Calculates the daily change in price
def get_price_changes(tickers):
    opens = get_opening_prices(tickers)
    currents = get_current_prices(tickers)

    changes = {}

    # Loop for each ticker calculating change from opening to current price
    for ticker in tickers:
        o = opens.get(ticker)
        c = currents.get(ticker)

        if o is None or c is None:
            changes[ticker] = None
        else:
            changes[ticker] = (c - o)

    return changes
    
# Main Run Loop
def main():
    if config["tui_on"]:
        print("Tui Active")

        while True:
            try:
                holdings = load_holdings()
                tickers = list(holdings.keys())

                # Main Print loop in tui.py
                print_total(holdings, get_current_prices(tickers), get_price_changes(tickers))

                # Refresh rate based on config
                time.sleep(config["update_time"])

            # Escape command
            except KeyboardInterrupt:
                print("\nQuitting HexenFolio")
                break
    else:
        print("Tui Not Active")

if __name__ == "__main__":
    main()