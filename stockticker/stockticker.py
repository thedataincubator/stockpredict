"""stockticker app"""
from datetime import datetime, timedelta
import requests
from requests import Timeout
import simplejson as json
from flask import Flask, render_template
from flask import  request # pylint: disable=W0611
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
import io
import zipfile
#static
static_valid_tickers = pd.DataFrame()

class QuandlException(Exception):
    """Exception for Quandl API"""
    pass

def update_valid_ticker(quandl_key):
    '''Uptate the dataframe for valid ticker'''
    params = {'api_key': quandl_key}
    try:
        r = requests.get('https://www.quandl.com/api/v3/databases/WIKI/codes',
                         params=params, timeout=10)
    except Timeout:
        raise QuandlException('Request timed out')
    if not r.ok:
        raise QuandlException('Request failed with status code {}'.format(r.status_code))
    file = zipfile.ZipFile(io.BytesIO(r.content)).read('WIKI-datasets-codes.csv')
    static_valid_tickers = pd.read_csv(io.BytesIO(file), names=['name', 'info'],
    usecols=[0], squeeze=True).str.slice(start=5)
    return static_valid_tickers

def check_valid_ticker(ticker):
    '''Validate the ticker'''
    if ticker in static_valid_tickers.values:
        return True
    else:
        raise QuandlException('The inputed ticker is not valid')
        return False

def query_quandl(ticker, quandl_key, value='open', days=500):
    """get stock value from quandl"""
    # prepare date string for the Quandl API
    date = (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%d')
    params = {'ticker': ticker, 'date.gte': date,
              'qopts.columns': 'date,{}'.format(value), 'api_key': quandl_key}
    try:
        r = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json', # pylint: disable=C0103
                         params=params, timeout=10)
    except Timeout:
        raise QuandlException('Request timed out')
    if not r.ok:
        raise QuandlException('Request failed with status code {}'.format(r.status_code))
    # we can catch more exceptions below, like JSONDecodeError, KeyError, etc.
    raw = json.loads(r.text)
    df = pd.DataFrame(raw['datatable']['data'], # pylint: disable=C0103
                      columns=[col['name'] for col in raw['datatable']['columns']])
    return df[['date', value]].rename({'date': 'ds', value: 'y'}, axis=1)

def create_app(prophet_url, secret_key, quandl_key, bokeh_version): # pylint: disable=W0613
    """create a flask app"""
    app = Flask(__name__)

    @app.route('/')
    def index(): # pylint: disable=W0612
        """main route"""
        if len(static_valid_tickers) < 1 :
            static_valid_tickers = update_valid_ticker(quandl_key)
        # Replace with Quandl API call on user input - may need to edit test
        df = pd.read_csv('static/GOOGL_data.txt') # pylint: disable=C0103

        # clean up reading into parameters
        params = dict(ds=[str(i) for i in df['ds'].values],
                      y=[str(i) for i in df['y'].values],
                      key=secret_key)

        # Handle different errors better from post request
        r = requests.post(prophet_url, data=json.dumps(params)) # pylint: disable=C0103
        if not r.ok:
            text = "<p>Sorry, you had error {}</p>".format(r.status_code)
            return render_template('index.html', div=text), r.status_code
        # Do we need error handling on this?
        prediction = pd.DataFrame(json.loads(r.text))
        prediction['ds'] = pd.to_datetime(prediction['ds'])
        df['ds'] = pd.to_datetime(df['ds'])
        # also show errors
        fig = figure(x_axis_type="datetime")
        fig.line(prediction['ds'].values,
                 prediction['yhat'].values,
                 line_color='red')
        fig.line(df['ds'].values, df['y'].values)
        script, div = components(fig)
        return render_template('index.html', script=script, div=div, bokeh=str(bokeh_version))

    return app
