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

class QuandlException(Exception):
    pass

def query_quandl(ticker, quandl_key, value='open', days=100):
    days = min(days, 800) # getting much larger than this causes too long URI

    # prepare date string for the Quandl API
    today = datetime.today()
    dates = ','.join((today-timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1,days+1))
    params = {'ticker': ticker, 'date': dates, 'api_key': quandl_key}
    try:
        r = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json',
                         params=params, timeout=10)
    except Timeout:
        raise QuandlException('Request timed out')
    if r.status_code != 200:
        raise QuandlException('Request failed with status code {}'.format(r.status_code))
    # we can catch more exceptions below, like JSONDecodeError, KeyError, etc.
    raw = json.loads(r.text)
    # raw['datatable']['data'] = [['GOOGL', '2018-03-22', 1080.01, 1083.92, ...], ...]
    df = pd.DataFrame(raw['datatable']['data'],
                        columns=[col['name'] for col in raw['datatable']['columns']])
    return df[['date', value]].rename({'date': 'ds', value: 'y'}, axis=1)

def create_app(prophet_url, secret_key, quandl_key, bokeh_version):
    """create a flask app"""
    app = Flask(__name__)

    @app.route('/')
    def index(): # pylint: disable=W0612
        """main route"""
        # Add user input?
        df = query_quandl('GOOGL', quandl_key, 'open', 100) # pylint: disable=C0103

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
