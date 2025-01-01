import os, logging
from pika.exceptions import AMQPError
import json
from ..channel import channel

stream_name=os.environ.get('RABBITMQ_STREAM')

def send_user_data_update(message: dict):
  try:
    channel.basic_publish(exchange='', routing_key=stream_name, body=json.dumps(message))
    print ("cloudamqp: Message sent to consumer")
  except AMQPError as e:
    logging.exception(e)
