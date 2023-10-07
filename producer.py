from confluent_kafka import Producer, KafkaException
import json
import time
import random

kafka_servers = "kafka-hub-cluster-kafka-bootstrap.kafka-streaming.svc.cluster.local:9092"
topic = "lobby"

def on_delivery(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def create_access_log_payload(record_id):
    # Create your AccessLog payload
    access_log = {
        "recordId": record_id,
        "personId": random.randint(10000, 99999),
        "entryTime": "2023-10-06T14:30:00",
        "exitTime": "2023-10-06T16:30:00",
        "destination": "1"
    }
    return json.dumps(access_log)

def check_kafka_connection(p):
    try:
        # Attempt to retrieve metadata for the specified topic
        metadata = p.list_topics(topic)
    except KafkaException as e:
        print(f'Failed to retrieve metadata for topic {topic}: {e}')
        return False
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return False
    return True

def main():
    p = Producer({'bootstrap.servers': kafka_servers})

    # Check connection to Kafka
    if not check_kafka_connection(p):
        print('Failed to connect to Kafka. Exiting...')
        return

    record_id = 1  # Initialize record_id
    while True:  # Infinite loop to keep sending messages every minute
        access_log_payload = create_access_log_payload(record_id)
        p.produce(topic, value=access_log_payload, callback=on_delivery)
        p.flush()  # Wait for any outstanding messages to be delivered and delivery report callbacks to be triggered.
        time.sleep(60)  # Sleep for 60 seconds before sending the next message
        record_id += 1  # Increment record_id for the next message

if __name__ == "__main__":
    main()
