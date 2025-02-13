import pika, os
import ssl

ENVIRONMENT = os.environ.get("ENVIRONMENT", default="production" )

# i was having an issue with an SSLEOFerror. 
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2

url = os.environ.get('CLOUDAMQP_URL') if ENVIRONMENT == 'production' else "amqp://guest:guest@rabbitmq:5672/"

params = pika.URLParameters(url)
params.heartbeat = 0 # setting heartbeat to zero to stop heartbeat timeout error

if ENVIRONMENT == 'production':
  params.ssl_options=pika.SSLOptions(context=ssl_context) 

connection = pika.BlockingConnection(params)
channel = connection.channel()