import os
from .channel import channel

# stream declaration
stream_name=os.environ.get('RABBITMQ_STREAM')
channel.queue_declare(queue=stream_name, durable=True, arguments={
  "x-queue-type": "stream", 
  "x-max-age": "1D",
  "x-max-length-bytes": 5000000, 
  "x-stream-max-segment-size-bytes":5000
  }) 