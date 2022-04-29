#!/usr/bin/python3

import tweepy
import json
import uuid
import time
from kafka import KafkaProducer


# Security: Extract API keys from separate file
with open("keys.txt") as f:
  lines = f.readlines()

auth = {}
for line in lines:
  name, key = line.split()
  auth[name] = key

# initialize kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# streaming filtering rules
rules = [tweepy.StreamRule("(bitcoin OR BTC) buy -sell lang:en", "BTC"),
         tweepy.StreamRule("(ethereum OR ETH) buy -sell lang:en", "ETH"),
         tweepy.StreamRule("(dogecoin OR DOGE) buy -sell lang:en", "DOGE")
         ]

# custom data handling
class GetTweets(tweepy.StreamingClient):
    def on_data(self, raw_data):
        """
        ex raw_data: {'data': {'id': '1519049905653833730', 'text': '@rovercrc At 100k they will buy some'}, 'matching_rules': [{'id': '1518908867291320322', 'tag': 'BTC'}]}
        ex msg: {"uuid": "cb72dea4-c5fd-11ec-975d-0242ac1c0002", "coin": "ETH", "time": 1651046086.2908614}
        """
        data = json.loads(raw_data)
        for rule in data['matching_rules']:
            tag = rule['tag']
            msg = f'{{"uuid": "{uuid.uuid1()}", "coin": "{tag}", "time": {time.time()}}}'
            producer.send("twitter", value=msg.encode('utf-8'))
        return True

twitter_stream = GetTweets(bearer_token=auth['twitter'])
twitter_stream.add_rules(rules, dry_run=False)


# start streaming
twitter_stream.filter()
