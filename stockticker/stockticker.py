"""stockticker app"""
from datetime import datetime, timedelta
import requests
from requests import Timeout
import simplejson as json
from flask import Flask, render_template, url_for, jsonify
from flask import  request # pylint: disable=W0611
import pandas as pd
from .stockplot import plotting

QUANDL_URL = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json'

class QuandlException(Exception):
    """Exception for Quandl API"""
    pass

def query_quandl(ticker, quandl_key, value='open', days=500):
    """get stock value from quandl"""

    # prepare date string for the Quandl API
    date = (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%d')
    params = {'ticker': ticker, 'date.gte': date,
              'qopts.columns': 'date,{}'.format(value), 'api_key': quandl_key}
    try:
        r = requests.get(QUANDL_URL, params=params, timeout=10)# pylint: disable=C0103
    except Timeout:
        raise QuandlException('Request timed out')
    if not r.ok:
        raise QuandlException('Request failed with status code {}'.format(r.status_code))
    # we can catch more exceptions below, like JSONDecodeError, KeyError, etc.
    raw = json.loads(r.text)
    df = pd.DataFrame(raw['datatable']['data'], # pylint: disable=C0103
                      columns=[col['name'] for col in raw['datatable']['columns']])
    return df[['date', value]].rename({'date': 'ds', value: 'y'}, axis='columns')

def query_prophet(prophet_url, secret_key, dates, prices):
    """Makes a query to Prophet"""
    prophet_params = {'ds': dates, 'y': prices, 'key': secret_key}

    return requests.post(prophet_url, data=json.dumps(prophet_params))

def get_error_div(error_string):
    """Returns a div displaying an error message"""
    return "<div>" + error_string + "</div>"

def get_initial_js(ticker_handler_url, portfolio_handler_url,
                   show_portfolio, ticker_params):
    """Build the JavaScript that will be executed when the page loads. This
    calls the JS function proccessTickers that accepts an array of ticker data,
    and fires off requests to get the ticker data. The function also has the
    URLs that initially handle these requests"""

    js_list = []
    js_list.append('<script type=text/javascript>')
    js_list.append('$(function() { ')
    js_list.append('stockTicker.processTickers(')
    js_list.append(json.dumps(show_portfolio))
    js_list.append(', ')
    js_list.append(json.dumps(ticker_params))
    js_list.append(', \'')
    js_list.append(ticker_handler_url)
    js_list.append('\', \'')
    js_list.append(portfolio_handler_url)
    js_list.append('\')});')
    js_list.append('</script>')
    return ''.join(js_list)

def create_app(prophet_url, secret_key, quandl_key, bokeh_version): # pylint: disable=W0613
    """create a flask app"""
    app = Flask(__name__)

    @app.route('/_handle_portfolio', methods=['POST'])
    def handle_portfolio():  # pylint: disable=W0612
        """Handles a POST request with a list of dates and
        corresponding prices"""
        dates = request.form['dates'].split(',')
        prices = request.form['prices'].split(',')
        counter = int(request.form['counter'])

        req = query_prophet(prophet_url, secret_key, dates, prices)

        if not req.ok:
            error_string = "Prophet error: " + str(req.status_code)
            return jsonify(div=get_error_div(error_string))

        prediction = pd.DataFrame(json.loads(req.text))
        prediction['ds'] = pd.to_datetime(prediction['ds'])
        df = pd.DataFrame()
        df['ds'] = pd.to_datetime(dates)
        df['y'] = pd.Series(prices, dtype=float)

        script, div = plotting(prediction, df)
        return jsonify(script=script, div=div, counter=counter)

    @app.route('/_handle_ticker')
    def handle_ticker(): # pylint: disable=W0612
        """Reads a ticker from the GET request, looks up the relevant data
        from Quandl, adds Prophet predictions, passes the data through Bokeh
        and then returns the Bokeh JavaScript and div via JSON"""

        ticker = request.args.get('ticker', type=str)
        counter = request.args.get('counter', type=int)

        df = query_quandl(ticker, quandl_key)
        # clean up reading into parameters
        params = dict(ds=[str(i) for i in df['ds'].values],
                      y=[str(i) for i in df['y'].values],
                      key=secret_key)

        # Handle different errors better from post request
        r = requests.post(prophet_url, data=json.dumps(params)) # pylint: disable=C0103
        if not r.ok:
            error_string = "Sorry, you had error {}".format(r.status_code)
            return jsonify(div=get_error_div(error_string))

        # Do we need error handling on this?
        prediction = pd.DataFrame(json.loads(r.text))
        prediction['ds'] = pd.to_datetime(prediction['ds'])
        df['ds'] = pd.to_datetime(df['ds'])
        # also show errors
        script, div = plotting(prediction, df)
        partial_results = {'dates': params['ds'],
                        'prices': [float(y) for y in params['y']]}
        return jsonify(script=script, div=div, ticker=ticker, counter=counter,
                       partialResults=partial_results)

    @app.route('/')
    def index(): # pylint: disable=W0612
        """main route"""
        ticker_handler_url = url_for('handle_ticker', _external=True)
        portfolio_handler_url = url_for('handle_portfolio', _external=True)
        stock_script_url = url_for('static', filename='stockTicker.js',
                                   _external=True)

        tickers = [{'ticker': 'GOOG', 'weight': .75},
                   {'ticker': 'AAPL', 'weight': .25}]
        show_portfolio = True

        query_script = get_initial_js(ticker_handler_url, portfolio_handler_url,
                                      show_portfolio, tickers)

        return render_template('index.html', stockscript=stock_script_url,
                               queryscript=query_script,
                               bokeh=str(bokeh_version))

    return app
