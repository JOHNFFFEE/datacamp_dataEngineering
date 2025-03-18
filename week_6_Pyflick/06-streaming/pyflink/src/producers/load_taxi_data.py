import csv
import json
from kafka import KafkaProducer
from time import time


def main():
    # Create a Kafka producer

    server = 'localhost:9092'
    topic_name = 'green-trips'

    producer = KafkaProducer(
        bootstrap_servers= [server],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    csv_file = '../data/green_tripdata_2019-10.csv'  # change to your CSV file path if needed

    # Define the columns you want to keep
    columns_to_keep = ['lpep_pickup_datetime', 'lpep_dropoff_datetime',
                       'PULocationID', 'DOLocationID', 'passenger_count',
                       'trip_distance', 'tip_amount']
    
    # Start timing
    t0 = time()


    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for message in reader:
            # Keep only required columns
            filtered_message = {key: message[key] for key in columns_to_keep}

            # Send message to Kafka topic
            producer.send(topic_name, value=filtered_message)
            print(f"Sent: {message}")

    # Make sure any remaining messages are delivered
    producer.flush()
    producer.close()
    t1 = time()
    print(f'Took {(t1 - t0):.2f} seconds')


if __name__ == "__main__":
    main()
