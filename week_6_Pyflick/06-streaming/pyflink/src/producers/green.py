import json
import pandas as pd

from kafka import KafkaProducer

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

server = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=json_serializer
)
file = './csv_file/green_tripdata_2019-10.csv'

df = pd.read_csv('file')



producer.bootstrap_connected()