"""stockticker app"""
from datetime import datetime, timedelta
import requests
from requests import Timeout
import simplejson as json
from flask import Flask, render_template, url_for, jsonify
from flask import  request # pylint: disable=W0611
import pandas as pd
from .stockplot import plotting
from .static_ticker import VALIDT
from .portfolio import sum_portfolio_data, parse_portfolio_args

QUANDL_URL = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json'

class QuandlException(Exception):
    """Exception for Quandl API"""
    pass

def ticker_precheck(ticker):
    """comvert ticker format and check its existence"""
    ticker = ''.join(ticker.upper().split())
    return ticker if ticker in VALIDT else 'GOOGL'

def query_quandl(ticker, quandl_key, value='open', days=500,
                 price_column_name='y'):
    """get stock value from quandl"""

    # prepare date string for the Quandl API
    date = (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%d')
    params = {'ticker': ticker, 'date.gte': date,
              'qopts.columns': 'date,{}'.format(value), 'api_key': quandl_key}
    try:
        req = requests.get(QUANDL_URL, params=params,
                           timeout=10)# pylint: disable=C0103
    except Timeout:
        raise QuandlException('Request timed out')
    if not req.ok:
        error = 'Request failed with status code {}'.format(req.status_code)
        raise QuandlException(error)
    # we can catch more exceptions below, like JSONDecodeError, KeyError, etc.
    raw = json.loads(req.text)
    df = pd.DataFrame(raw['datatable']['data'], # pylint: disable=C0103
                      columns=[col['name'] for col
                               in raw['datatable']['columns']])
    return df[['date', value]].rename({'date': 'ds', value: price_column_name},
                                      axis='columns')

def get_portfolio_data(tickers, weights, quandl_key):
    """Given the tickers and weights, queries Quandl for the stock data
    and returns a dataframe with the weighted porfolio value"""

    for i, ticker in enumerate(tickers):
        stock_data = query_quandl(ticker, quandl_key, price_column_name=ticker)
        if i == 0:
            portfolio_data = stock_data
        else:
            portfolio_data[ticker] = stock_data[ticker]

    sum_portfolio_data(portfolio_data, tickers, weights)

    return portfolio_data

def get_prophet_plot(prophet_url, secret_key, dates, prices):
    """Passes the given prices and dates to prophet, produces
    a Bokeh plot with the data and prediction, and returns the
    script and div for the plot"""
    req = query_prophet(prophet_url, secret_key, dates, prices)

    if not req.ok:
        return "", get_error_div("Prophet Error")

    data = pd.DataFrame()
    data['ds'] = pd.to_datetime(dates)
    data['y'] = pd.Series(prices, dtype=float)

    prediction = pd.DataFrame(json.loads(req.text))
    prediction['ds'] = pd.to_datetime(prediction['ds'])

    return plotting(prediction, data)

def query_prophet(prophet_url, secret_key, dates, prices):
    """Makes a query to Prophet"""
    prophet_params = {'ds': dates, 'y': prices, 'key': secret_key}

    return requests.post(prophet_url, data=json.dumps(prophet_params))

def get_error_div(error_string):
    """Returns a div displaying an error message"""
    return "<div>" + error_string + "</div>"

def create_app(prophet_url, secret_key, quandl_key,
               bokeh_version): # pylint: disable=W0613
    """create a flask app"""
    app = Flask(__name__)

    @app.route('/portfolio')
    def portfolio():  # pylint: disable=W0612
        """Portfolio route: Accepts a list of tickers and a list of weights.
        Example: portfolio?tickers=GOOGL,AAPL&weights=.25,.75"""

        tickers, weights = parse_portfolio_args(request)

        portfolio_data = get_portfolio_data(tickers, weights, quandl_key)
        dates = [str(i) for i in portfolio_data['ds'].values]
        prices = [str(i) for i in portfolio_data['Portfolio'].values]

        script, div = get_prophet_plot(prophet_url, secret_key, dates, prices)

        return render_template('portfolio.html', bokeh_script=script,
                               bokeh_div=div, bokeh=str(bokeh_version))


    @app.route('/_handle_ticker')
    def handle_ticker(): # pylint: disable=W0612
        """Reads a ticker from the GET request, looks up the relevant data
        from Quandl, adds Prophet predictions, passes the data through Bokeh
        and then returns the Bokeh JavaScript and div via JSON"""

        ticker = request.args.get('ticker', type=str)
        valid_ticker = ticker_precheck(ticker)

        counter = request.args.get('counter', type=int)

        data = query_quandl(valid_ticker, quandl_key)

        dates = [str(i) for i in data['ds'].values]
        prices = [str(i) for i in data['y'].values]

        script, div = get_prophet_plot(prophet_url, secret_key, dates, prices)
        return jsonify(ticker=ticker, script=script, div=div, counter=counter)

    @app.route('/')
    def index(): # pylint: disable=W0612
        """main route"""
        ticker_list = request.args.get('tickers', type=str)

        if ticker_list:
            initial_tickers = [{'ticker': ticker} for ticker in
                               ticker_list.split(',')]
        else:
            initial_tickers = []

        ticker_query_url = url_for('handle_ticker', _external=True)
        stock_script_url = url_for('static', filename='stockTicker.js',
                                   _external=True)

        return render_template('index.html',
                               stock_script_url=stock_script_url,
                               ticker_query_url=ticker_query_url,
                               initial_tickers=json.dumps(initial_tickers),
                               bokeh=str(bokeh_version))
    return app
