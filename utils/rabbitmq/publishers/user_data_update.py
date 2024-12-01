import pika, os, logging
from pika.exceptions import AMQPError
import json
import ssl

# i was having an issue with an SSLEOFerror. 
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2

url = os.environ.get('CLOUDAMQP_URL')
params = pika.URLParameters(url)

# i was having an issue with an SSLEOFerror. 
params.ssl_options=pika.SSLOptions(context=ssl_context) 

user_data_update_queue = os.environ.get('CLOUDAMQP_USER_DATA_UPDATE_QUEUE')

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(user_data_update_queue)

def send_user_data_update(message: dict):
  try:
    channel.basic_publish(exchange='', routing_key=user_data_update_queue, body=json.dumps(message))
    print ("cloudamqp: Message sent to consumer")
    # connection.close()
  except AMQPError as e:
    logging.exception(e)
