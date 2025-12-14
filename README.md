# HexFolio

This is a self hosted stock portfolio viewing dashboard meant to run as a docker container. This program adds up your total holdings as listed in the holdings.yaml file and hosts them on a local site which graphs their movements live.

## Use
Put your holdings in holdings.yaml (As seen in the example, under tickers you put TICKER: NUMBER-HELD) as well as your prefered port, then open the page on your device of choice. 

## Future Feature Ideas
- Button to add a ticker and quantity (ruamel.yaml looks good for this)
- Swappable themes
- NTFY integration for movement notifications (Daily recaps or price spike events)

## Feature List

#### Version 0.1.0
- Minimum Viable Product
- Uses the given YAML portfolio and calculates the total and continuously prints it in the terminal
- Bare bones back end to build on essentially
