from confluent_kafka import Consumer
import click
import io
import signal
from fastavro import reader

print("script is running!")

c = Consumer({
    'bootstrap.servers': '13.49.128.80:19093,13.49.128.80:29093,13.49.128.80:39093',
    'group.id': 'group4',
    'auto.offset.reset': 'smallest',
    'security.protocol': 'SSL',
    'ssl.ca.location': './ca.crt',
    'ssl.keystore.location': './kafka.keystore.pkcs12',
    'ssl.keystore.password': 'cc2023',
    'enable.auto.commit': 'true',
    'ssl.endpoint.identification.algorithm': 'none',
})

print("consumer created!")


def signal_handler(sig, frame):
    print('EXITING SAFELY!')
    exit(0)


signal.signal(signal.SIGTERM, signal_handler)


@click.command()
@click.argument('topic')
def consume(topic: str):
    c.subscribe(
        [topic],
        on_assign=lambda _, p_list: print(p_list)
    )
    try:
        while True:
            msg = c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            # headers = msg.headers()

            message_bytes = io.BytesIO(msg.value())
            avro_schema = reader(message_bytes)
            print(msg.headers()[0][1].decode("utf-8"))
            for i in avro_schema:
                print(i)
    except Exception as e:
        print(e)


consume()
