# Harvard University Extension School "Principles of Big Data Processing" Final Project

# Project Goal and Problem Statement
The project’s goal is to visualize the relationship between major cryptocurrencies’ price with their twitter mentions in real time. It will be interesting to see if the price movement precedes or follows twitter mentions.

# YouTube Video URL
https://www.youtube.com/watch?v=sz6n_7QhwS0
 
# DEMO Visualization:
http://3.133.137.61/public/dashboards/ywzotGg9jNlg975O15mcAGNQnWbWhYpJPf23KAnw?org_slug=default
 
# Dependency:
- Docker
- Cassandra
    - Modify cassandra.yaml to your host ip
- Kafka
- Faust
- Python
- Tweepy
- Twitter API Key
- CompareCrypto API Key

# Start the Pipeline:
1. Start ec2 instance from Redash AMI (t2.xlarge)
2. Start Kafka: docker-compose -f docker-compose-cryptotweetmap.yml up
3. Start Cassandra: ./apache-cassandra-4.0.3/bin/cassandra
4. Start Faust Twitter Worker: python3 tw_worker.py worker -l info
5. Start Faust Coin Worker: python3 coin_worker.py worker -l info --web-port 6067
6. (Optional) Test workers: python3 tw_worker.py send twitter '{"uuid": "cb72dea4-c5fd-11ec-975d-0242ac1c0002", "coin": "ETH", "time": 1651046086.2908614}'
7. (Optional) Test workers: python3 coin_worker.py send coinbase '{"uuid": "cb72dea4-c5fd-11ec-975d-0242ac1c0002", "coin": "BTC", "time": 1651046086.2908614, "quote": 38342.44}'
8. Start collecting twitter data: python3 cryptotweet.py
9. Start collecting quotes: python3 cryptoprice.py
10. Configure Redash: http://your_ec2_public_ip/
    - Useful tutorial by Redash: https://www.youtube.com/watch?v=Yn3_QDk2qQM&t=186s

by: Jack Tsu