import asyncio
import argparse
import json
from datetime import datetime

import faust
from kafka import KafkaProducer


TOPIC = "greetings"


app = faust.App(
    "hello-world-producer",
    broker="kafka://kafka:9092",
)


class Greeting(faust.Record):
    message: str
    timestamp: datetime


greetings_topic = app.topic(TOPIC, value_type=Greeting)


async def greet(message):
    await greetings_topic.send(
        value=Greeting(
            message=" ".join(message),
            timestamp=datetime.now(),
        )
    )


async def async_main(message):
    await greet(message)
    await app.producer.stop()


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


def main(message):
    kafka_producer = create_kafka_producer()
    greeting = {
        "message": " ".join(message),
    }
    publish_message(kafka_producer, TOPIC, "key", json.dumps(greeting))
    if kafka_producer is not None:
        kafka_producer.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("message", nargs="*")
    args = parser.parse_args()

    # main(args.message)
    asyncio.run(async_main(args.message))
