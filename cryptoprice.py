#!/usr/bin/python3

import requests
import time
import uuid
from kafka import KafkaProducer


# initiate kafka
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

class GetQuote():
  def __init__(self):
    self.key = "784ea39f1aa31ca58a52302fb09629283f0fb4fdde5dddb27cd4a547f70668ac"
  
  def get_quotes(self):
    """
    ex raw_data: {"ETH":{"BTC":0.07399,"USD":2877.55,"EUR":2715.57},"DASH":{"BTC":0.002448,"USD":95.21,"EUR":89.82}}
    ex msg: {"uuid": "cb72dea4-c5fd-11ec-975d-0242ac1c0002", "coin": "ETH", "time": 1651046086.2908614, "quote": 38342.44}
    """
    data = requests.get(f"https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH,DOGE&tsyms=USD&api_key={self.key}").json()
    quotes = [('BTC', data['BTC']['USD']), ('ETH', data['ETH']['USD']), ('DOGE', data['DOGE']['USD'])]
    for quote in quotes:
      msg = f'{{"uuid": "{uuid.uuid1()}", "coin": "{quote[0]}", "time": {time.time()}, "quote": {quote[1]}}}'
      producer.send("coinbase", value=msg.encode('utf-8'))
    time.sleep(5)

  def stream(self):
    while True:
      self.get_quotes()


# start streaming
quote_stream = GetQuote()
quote_stream.stream()
