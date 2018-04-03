"""app to predict stock prices"""
import os
import requests
import simplejson as json
from flask import Flask, render_template
from flask import request # pylint: disable=W0611
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__) # pylint: disable=C0103

PROPHET_URL = os.environ['PROPHET_URL']
SECRET_KEY = os.environ['SECRET_KEY']

@app.route('/')
def index():
    """index of site, queries the backend model"""
    # Replace with API call to quandle
    data_frame = pd.read_csv('static/GOOGL_data.txt')

    # clean up reading into parameters
    params = dict(ds=[str(i) for i in data_frame['ds'].values],
                  y=[str(i) for i in data_frame['y'].values],
                  key=SECRET_KEY)

    # handle errors from post request
    prediction = requests.post(PROPHET_URL, data=json.dumps(params))

    # Do we need error handling on this?
    prediction = pd.DataFrame(json.loads(prediction.text))
    prediction['ds'] = pd.to_datetime(prediction['ds'])
    data_frame['ds'] = pd.to_datetime(data_frame['ds'])
    # also show errors
    fig = figure(x_axis_type="datetime")
    fig.line(prediction['ds'].values,
             prediction['yhat'].values,
             line_color='red')
    fig.line(data_frame['ds'].values, data_frame['y'].values)
    script, div = components(fig)
    return render_template('index.html', script=script, div=div)

if __name__ == '__main__':
    app.run(port=33507)
