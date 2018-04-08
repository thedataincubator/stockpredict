import os
from stockticker import create_app

PROPHET_URL = os.environ['PROPHET_URL']
SECRET_KEY = os.environ['SECRET_KEY']
QUANDL_KEY = os.environ['QUANDL_KEY']
BOKEH_VERSION = os.environ.get('BOKEH_VERSION_NUMBER', '7')

static_valid_tickers = []
app = create_app(PROPHET_URL, SECRET_KEY, QUANDL_KEY, BOKEH_VERSION)

if __name__ == '__main__':
  app.run(port=33507)
