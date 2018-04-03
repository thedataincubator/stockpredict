import os
import requests
import simplejson as json
from flask import Flask, render_template, request, redirect
import pandas as pd 
from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__)

PROPHET_URL = os.environ['PROPHET_URL']
SECRET_KEY = os.environ['SECRET_KEY']

@app.route('/')
def index():
  # TODO Replace with API call to quandle
  df = pd.read_csv('static/GOOGL_data.txt')

  # TODO clean up reading into parameters
  params = dict(ds=[str(i) for i in df['ds'].values], 
                y=[str(i) for i in df['y'].values],
                key=SECRET_KEY)

  # TODO handle errors from post request
  r = requests.post(PROPHET_URL, data=json.dumps(params))

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

if __name__ == '__main__':
  app.run(port=33507)