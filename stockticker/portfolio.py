"""Portfolio processing"""

def sum_portfolio_data(portfolio_data, tickers, weights):
    """Sum the data in the portfolio data frame"""

    def _add_columns(row):
        """Adds the stock data for a given row"""
        if not weights:
            return sum(row[ticker] for ticker in tickers)
        return sum(row[ticker]*weights[ticker] for ticker in tickers)

    portfolio_data['Portfolio'] = portfolio_data.apply(_add_columns, axis=1)

def parse_portfolio_args(request):
    """Parse the args to the portfolio route"""

    tickers = request.args.get('tickers', type=str)
    if tickers:
        tickers = tickers.split(',')
    else: #For now, just use a default portfolio if nothing is specified
        tickers = ['GOOGL', 'AAPL']

    weights = request.args.get('weights', type=str)
    print("before", weights)
    if weights:
        weights = weights.split(',')
        weights = {tickers[i]: float(weights[i]) for i in range(len(tickers))}
        print("weights", weights)
    else:
        weights = None


    return (tickers, weights)


