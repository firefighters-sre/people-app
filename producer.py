from confluent_kafka import Producer
import json

kafka_servers = "kafka-hub-cluster-kafka-bootstrap.kafka-streaming.svc.cluster.local:9092"
topic = "lobby"

def on_delivery(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def create_access_log_payload():
    # Create your AccessLog payload
    access_log = {
        "recordId": 1,
        "personId": 12345,
        "entryTime": "2023-10-06T14:30:00",
        "exitTime": "2023-10-06T16:30:00",
        "destination": "Floor 1"
    }
    return json.dumps(access_log)

def main():
    p = Producer({'bootstrap.servers': kafka_servers})
    access_log_payload = create_access_log_payload()
    p.produce(topic, value=access_log_payload, callback=on_delivery)
    p.flush()  # Wait for any outstanding messages to be delivered and delivery report callbacks to be triggered.

if __name__ == "__main__":
    main()