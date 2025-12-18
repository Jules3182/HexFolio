import time
import math
from app.utils.validation import is_valid_price
from app.core.config import CONFIG
from app.services.holdings_service import get_holdings
from app.services.pricing_service import (
    get_opening_prices,
    get_current_prices,
    get_price_changes,
    get_price_changes_percent
)

# Rich stuff for live updates and console
from rich.live import Live
from rich.console import Console

# Terminal management stuff moved to other file
from tui import portfolio_table

# Main Run Loop
def main():
    # Checking if TUI is disabled in config
    if not CONFIG["tui_on"]:
        print("Tui Not Active")
        return

    # Setting up variables for easy passing in
    console = Console()
    holdings = get_holdings()

    try:

        opens_cache = get_opening_prices(holdings)
        
        # Live loop for constantly refreshing TUI tables
        with Live(
            portfolio_table(holdings, {}, {}, {}),
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
                    portfolio_table(
                        holdings,
                        current_prices,
                        price_changes,
                        price_changes_percent
                    )
                )

                # Updates at user configured speed
                time.sleep(CONFIG["update_time"])

    # Exit case and little "sign off" print
    except KeyboardInterrupt:
        console.print("\n[bold red]Quitting HexFolio TUI[/]")

if __name__ == "__main__":
    main()