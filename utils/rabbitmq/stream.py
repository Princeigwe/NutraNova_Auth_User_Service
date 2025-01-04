import os
from .channel import channel

# stream declaration
stream_name=os.environ.get('RABBITMQ_STREAM')
channel.queue_declare(queue=stream_name, durable=True, arguments={"x-queue-type": "stream", "x-max-age": "7D"}) ## message in the stream queue is set to delete after 7 days