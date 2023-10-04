from mongoengine import *
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi 
import pika
import time
from models import *

 
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='task_campaing', durable=True)

def callback(ch, method, properties, body):
      pk = body.decode()
      task = Contact.objects(id=pk ).first()
       
      if task :
        time.sleep(0.5)
         
        print(f"send contakt id  { pk }, on  email  ")
      
  
      ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_campaing', on_message_callback=callback)

if __name__ == '__main__':
    channel.start_consuming()
 