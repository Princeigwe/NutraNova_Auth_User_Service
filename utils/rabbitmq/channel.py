import pika, os
import ssl

# i was having an issue with an SSLEOFerror. 
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2

url = os.environ.get('CLOUDAMQP_URL')

params = pika.URLParameters(url)
params.heartbeat = 0 # setting heartbeat to zero to stop heartbeat timeout error
params.ssl_options=pika.SSLOptions(context=ssl_context) 

connection = pika.BlockingConnection(params)
channel = connection.channel()