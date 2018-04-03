import os
from stockticker import create_app

PROPHET_URL = os.environ['PROPHET_URL']
SECRET_KEY = os.environ['SECRET_KEY']

app = create_app(PROPHET_URL, SECRET_KEY)

if __name__ == '__main__':
  app.run(port=33507)