import time
import os

from rich import print
from rich.table import Table
from rich.console import Console
from rich.live import Live

from app.services.holdings_service import get_holdings as hu
from app.services.pricing_service import (
    get_opening_prices,
    get_current_prices,
    get_price_changes,
    get_price_changes_percent
)


console = Console()

def portfolio_table(holdings: dict, prices, change, change_percent) -> Table:
    # Set up for the portfolio stats displayed in the terminal with rich
    table = Table(title="Portfolio Standings")

    table.add_column("Ticker", style="bold", no_wrap=True)
    table.add_column("Shares", no_wrap=True)
    table.add_column("Price ($)", no_wrap=True)
    table.add_column("Value ($)", no_wrap=True)
    table.add_column("Change ($)", no_wrap=True)
    table.add_column("Change (%)", no_wrap=True)
    # User config for what columns are shown?

    # Sets total variables
    total = 0
    total_change = 0.0
    total_change_percent = 0.0

    # Loops through each ticker pulling price and number of shares
    for ticker, shares in holdings.items():
        price = prices.get(ticker)
        delta = change.get(ticker)
        delta_percent = change_percent.get(ticker)

        # # resets total variables (there's definetly a smarter way of doing this)
        # total = 0
        # total_change = 0.0
        # total_change_percent = 0.0

        # Skip invalid/missing prices
        if price is None:
            continue

        # Handles the math
        value = price * shares
        total += value
        total_change += (delta * shares)

        # Messing aroind with visual Up/Down stuff with rich
        color = "green" if (delta >= 0) else "red"
        symbol = "▲" if (delta >= 0) else "▼"

        # Looping through tickers, pulling the data we need, and putting it in the right spots
        table.add_row(
            str(ticker),
            str(shares),
            f"{float(price):.2f}",
            f"{float(value):.2f}",
            f"[{color}]{symbol} ${abs(float(delta * shares)):.2f}",
            f"[{color}]{symbol} %{abs(float(delta_percent)):.2f}"
        )
        
        total_change_percent = ((total - (total - total_change)) / (total - total_change) * 100)
    
    # Stylimg for bottom rown, I will likely split this off into a new function later
    color = "green" if (total_change >= 0) else "red"
    symbol = "▲" if (total_change >= 0) else "▼"

    # Adds a row at the bottom for the total value and price change over the day
    table.add_section()
    table.add_row(
        "[bold]TOTAL[/]",
        "",
        "",
        f"[bold]{total:,.2f}[/]",
        f"[bold][{color}]{symbol} ${abs(total_change):,.2f}[/]",
        f"[bold][{color}]{symbol} %{abs(total_change_percent):,.2f}[/]"
    )

    return table