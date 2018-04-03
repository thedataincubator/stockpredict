import os
import requests
import simplejson as json
from flask import Flask, render_template, request, redirect
import pandas as pd 
from bokeh.plotting import figure
from bokeh.embed import components

def create_app(prophet_url, secret_key):
    app = Flask(__name__)

    @app.route('/')
    def index():
        # TODO Replace with API call to quandle
        df = pd.read_csv('static/GOOGL_data.txt')

        # TODO clean up reading into parameters
        params = dict(ds=[str(i) for i in df['ds'].values], 
                        y=[str(i) for i in df['y'].values],
                        key=secret_key)

        # TODO handle different errors better from post request
        r = requests.post(prophet_url, data=json.dumps(params))
        if not r.ok:
            text = "<p>Sorry, you had error {}</p>".format(r.status_code)
            return render_template('index.html', div=text), r.status_code
        # TODO Do we need error handling on this?
        prediction = pd.DataFrame(json.loads(r.text))
        prediction['ds'] = pd.to_datetime(prediction['ds'])
        df['ds'] = pd.to_datetime(df['ds'])
        # TODO also show errors
        fig = figure(x_axis_type="datetime")
        fig.line(prediction['ds'].values, 
                prediction['yhat'].values,
                line_color='red')
        fig.line(df['ds'].values, df['y'].values)
        script, div = components(fig)
        return render_template('index.html', script=script, div=div)
    
    return app