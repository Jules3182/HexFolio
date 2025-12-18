from app.core.config import HOLDINGS_DATA

# Service for cleanly returning holdings from one place
def get_holdings():
    return HOLDINGS_DATA["tickers"]