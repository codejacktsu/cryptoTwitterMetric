#!/usr/bin/python3

import faust
from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from datetime import datetime


# init
cluster = Cluster()
session = cluster.connect('cryptotwitter')
app = faust.App('coin_worker', broker='kafka://localhost:9092')

# Cassandra insert
def cassandra_coin_insert(values):
  query = f"INSERT INTO cryptotwitter.history (uuid, coin, type, quote, time) VALUES {values};"
  statement = session.prepare(query)
  statement.consistency_level = ConsistencyLevel.QUORUM
  session.execute(statement)
  print(f"sent: {values}")

# Faust
class Quotes(faust.Record):
  """
  {"uuid": "cb72dea4-c5fd-11ec-975d-0242ac1c0002", "coin": "ETH", "time": 1651046086.2908614, "quote": 38342.44}
  """
  uuid: str
  coin: str
  time: float
  quote: float

coin_topic = app.topic('coinbase', value_type=Quotes)

@app.agent(coin_topic)
async def quote(quotes):
  """
  Cassandra table: (uuid,coin,type,quote,time)
  """
  async for quote in quotes:
    time = datetime.fromtimestamp(quote.time).strftime('%Y-%m-%d %H:%M:%S')
    msg = f"({quote.uuid},'{quote.coin}','price',{quote.quote},'{time}')"
    # print(quote)
    # send to Cassandra
    cassandra_coin_insert(msg)


if __name__ == '__main__':
  app.main()
