# HexFolio

This is a self hosted stock portfolio viewing dashboard meant to run as a docker container. This program adds up your total holdings as listed in the holdings.yaml file and hosts them on a local site which graphs their movements live.

## Use
Put your holdings in holdings.yaml (As seen in the example, under tickers you put TICKER: NUMBER-HELD) as well as your prefered port, then open the page on your device of choice. 

## Future Feature Ideas
- Button to add a ticker and quantity (ruamel.yaml looks good for this)
- Swappable themes
- NTFY integration for movement notifications (Daily recaps or price spike events)

## Dev Roadmap:
1. Proof of concept
2. Functional TUI
3. Build in FastAPI so it can display basically the TUI on a webserver
4. Get Plotly.js working to display live graphs of the data
5. Dockerize the whole thing to work as a container
6. Expand on features, add customization, etc.

## Feature List

#### Version 0.1.2
- Full project structure has been reworked
- Essentially 2 scripts, split up into modules that make sense and are far more scalable
- Framework has been laid to get FastApi up and running
- I will polish up what is here, add a few small features and refine my backend and then move onto the frontend work!

#### Version 0.1.1
- Much better TUI!
- Uses rich for table, color, and live data
- Reworked a lot of the code to be more cohesive

#### Version 0.1.0
- Proof of concept really
- Uses the given YAML portfolio and calculates the total and continuously prints it in the terminal
- Bare bones back end to build on essentially
