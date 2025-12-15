import yaml
import yfinance as yf
import time
import math

# Rich stuff for live updates and console
from rich.live import Live
from rich.console import Console

# Utils split into other file for future use
from holdings_utils import add_ticker, remove_ticker, set_ticker_value

# Terminal management stuff moved to other file
import tui

# Caching prices to help not break when stocks are slow to update
price_cache: dict[str, float] = {}

# Checking if price is valid to stop slow to update prices from breaking math
def is_valid_price(value) -> bool:
    return value is not None and not math.isnan(value)

# Loads up user config on start
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Gets listed tickers from holdings.yaml
def load_holdings():
    with open("holdings.yaml", "r") as f:
        data = yaml.safe_load(f)
        return data["tickers"]

# Get opening prices for each ticker
# (I need to cache this somewhere and only call during market hours if data is old)
def get_opening_prices(holdings: dict):
    opening_prices = {}

    for ticker in holdings.keys():
        hist = yf.Ticker(ticker).history(period="1d", interval="1m")

        opening_prices[ticker] = (
            float(hist.iloc[0]["Open"]) if not hist.empty else None
        )

    return opening_prices

# Pulls stock price for each ticker
def get_current_prices(holdings: dict) -> dict[str, float] | None:
    global price_cache
    
    tickers = list(holdings.keys())

    # Actually gets the data from yfinance
    data = yf.download(
        tickers,
        period="1d",
        interval="1m",
        progress=False,
        auto_adjust=True
    )

    # Picks out the "close" price
    close = data["Close"].iloc[-1]
    prices = {}

    # Fix for dict's being passed into functions
    if hasattr(close, "to_dict"):
        close_dict = close.to_dict()
    else:
        close_dict = {tickers[0]: float(close)}

    # Loop for getting prices
    for ticker in tickers:
        price = close_dict.get(ticker)

        # Checks if price is valid
        if is_valid_price(price):
            price_cache[ticker] = float(price)
            prices[ticker] = float(price)
        else:
            # Uses last known price if invalid price is passed in (nan)
            prices[ticker] = price_cache.get(ticker)

    return prices

# Calculates the daily change in price
def get_price_changes(tickers):
    # Getting the open prices and current prices to compare
    opens = get_opening_prices(tickers)
    currents = get_current_prices(tickers)

    # List for changes in price
    changes = {}

    # Loop for each ticker calculating change from opening to current price
    for ticker in tickers:
        o = opens.get(ticker)
        c = currents.get(ticker)

        # Case for no change
        # (Doesn't have any use really yet but I will fix that)
        if o is None or c is None:
            changes[ticker] = None
        else:
            changes[ticker] = (c - o)

    return changes

# Calculates the daily change in price (will likely change this later to just be in the same function as other one)
def get_price_changes_percent(tickers):
    # Getting the open prices and current prices to compare
    opens = get_opening_prices(tickers)
    currents = get_current_prices(tickers)

    # List for changes in price
    changes = {}

    # Loop for each ticker calculating change from opening to current price
    for ticker in tickers:
        o = opens.get(ticker)
        c = currents.get(ticker)

        # Case for no change
        # (Doesn't have any use really yet but I will fix that)
        if o is None or c is None:
            changes[ticker] = None
        else:
            changes[ticker] = (((c - o) / o) * 100)

    return changes
    
# Main Run Loop
def main():
    # Checking if TUI is disabled in config
    if not config["tui_on"]:
        print("Tui Not Active")
        return

    # Setting up variables for easy passing in
    console = Console()
    holdings = load_holdings()

    try:

        opens_cache = get_opening_prices(holdings)
        
        # Live loop for constantly refreshing TUI tables
        with Live(
            tui.portfolio_table(holdings, {}, {}, {}),
            console=console,
            refresh_per_second=2,
        ) as live:

            while True:
                # Pulling most recent data to pass in
                current_prices = get_current_prices(holdings)
                price_changes = get_price_changes(holdings)
                price_changes_percent = get_price_changes_percent(holdings)

                # Refreshing the table with fresh data, realistically I should cache the holdings but I like this for now
                live.update(
                    tui.portfolio_table(
                        holdings,
                        current_prices,
                        price_changes,
                        price_changes_percent
                    )
                )

                # Updates at user configured speed
                time.sleep(config["update_time"])

    # Exit case and little "sign off" print
    except KeyboardInterrupt:
        console.print("\n[bold red]Quitting HexFolio TUI[/]")

if __name__ == "__main__":
    main()