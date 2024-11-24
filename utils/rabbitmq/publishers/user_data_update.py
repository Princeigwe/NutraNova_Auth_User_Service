import pika, os, logging
from pika.exceptions import AMQPError
import json

url = os.environ.get('CLOUDAMQP_URL')
params = pika.URLParameters(url)

user_data_update_queue = os.environ.get('CLOUDAMQP_USER_DATA_UPDATE_QUEUE')

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(user_data_update_queue)

def send_user_data_update(message: dict):
  try:
    channel.basic_publish(exchange='', routing_key=user_data_update_queue, body=json.dumps(message))
    print ("cloudamqp: Message sent to consumer")
    connection.close()
  except AMQPError as e:
    logging.exception(e)
