import click
import json

from kafka import KafkaProducer


TOPIC = "greetings"


def publish_message(producer, topic, key, value):
    try:
        key_bytes = bytes(key, encoding="utf-8")
        value_bytes = bytes(value, encoding="utf-8")
        producer.send(topic, key=key_bytes, value=value_bytes)
        producer.flush()
    except Exception as exc:
        print(exc)


def create_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(
            bootstrap_servers=["kafka:9092"],
        )
    except Exception as exc:
        print(exc)
    return _producer


@click.command()
@click.argument("message", nargs=-1)
def main(message):
    kafka_producer = create_kafka_producer()
    publish_message(kafka_producer, TOPIC, "key", " ".join(message))
    if kafka_producer is not None:
        kafka_producer.close()


if __name__ == "__main__":
    main()
