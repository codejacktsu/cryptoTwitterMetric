#!/usr/bin/python3

import faust
from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from datetime import datetime


# init
cluster = Cluster()
session = cluster.connect('cryptotwitter')
app = faust.App('tw_worker', broker='kafka://localhost:9092')

# Cassandra insert
def cassandra_tweet_insert(values):
  query = f"INSERT INTO cryptotwitter.history (uuid, coin, type, time) VALUES {values};"
  statement = session.prepare(query)
  statement.consistency_level = ConsistencyLevel.QUORUM
  session.execute(statement)
  print(f"sent: {values}")

# Faust
class Tweets(faust.Record):
  """
  {"uuid": "cb72dea4-c5fd-11ec-975d-0242ac1c0002", "coin": "ETH", "time": 1651046086.2908614}
  """
  uuid: str
  coin: str
  time: float

twitter_topic = app.topic('twitter', value_type=Tweets)

@app.agent(twitter_topic)
async def tweet(tweets):
  """
  Cassandra table: (uuid,coin,type,time)
  """
  async for tweet in tweets:
    time = datetime.fromtimestamp(tweet.time).strftime('%Y-%m-%d %H:%M:%S')
    msg = f"({tweet.uuid},'{tweet.coin}','tweet','{time}')"
    # print(tweet)
    # send to Cassandra
    cassandra_tweet_insert(msg)
    