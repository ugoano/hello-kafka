from datetime import datetime

import faust

app = faust.App(
    "hello-world",
    broker="kafka://kafka:9092",
)

class Greeting(faust.Record):
    message: str
    # timestamp: datetime = datetime.now()


greetings_topic = app.topic("greetings", value_type=Greeting)


@app.agent(greetings_topic)
async def greet(greetings: Greeting):
    async for greeting in greetings:
        print(greeting.message)
