import yfinance as yf
from app.utils.validation import is_valid_price

# Caching prices to help not break when stocks are slow to update
price_cache: dict[str, float] = {}

# Get opening prices for each ticker
# (I need to cache this somewhere and only call once during market hours if data is old)
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
   