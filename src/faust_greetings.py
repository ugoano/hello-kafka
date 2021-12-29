from datetime import datetime
from typing import List

import faust

app = faust.App(
    "hello-world",
    broker="kafka://kafka:9092",
)

class Greeting(faust.Record):
    message: str
    timestamp: datetime


greetings_topic = app.topic("greetings", value_type=Greeting)


@app.agent(greetings_topic)
async def greet(greetings: List[Greeting]):
    async for greeting in greetings:
        print(greeting.message)
        print(greeting.timestamp)
