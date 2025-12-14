import time
import os
from rich import print

from holdings_utils import load_holdings as hu


# Function to print values, will be updated to "update"
def print_total(holdings: dict, prices: dict, change: dict):
    # Sets total variable
    total = 0

    # Sets up breakdown list for use in print loop
    breakdown = []

    # Loops through each ticker pulling price and number of shares
    for ticker, shares in holdings.items():
        price = prices.get(ticker)
        delta = change.get(ticker)

        # Skip invalid/missing prices
        if price is None:
            continue

        # Does some math and then appends values in order to the breakdown list
        value = price * shares
        total += value
        breakdown.append((ticker, shares, price, value, delta))

    # Clears console
    os.system("cls" if os.name == "nt" else "clear")

    print("=$=$= Portfolio Total =$=$=")
    print(f"Total Value: ${total:,.2f}\n")

    # This should totally be turned into a table with rich later
    for ticker, shares, price, value, delta in breakdown:
        color = "green" if (delta >= 0) else "red"
        print(f"{ticker}: [{color}]{shares}[/{color}] x $ [{color}]{price:.2f}[/{color}] = [{color}]$ {value:,.2f}[/{color}], with a daily price change of [{color}] $ {delta:.2f}")