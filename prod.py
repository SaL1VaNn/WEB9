from mongoengine import *
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi 
from models import *
from faker import Faker
import pika



fake = Faker()
def maker_contacts():
     for _ in range(30):
          result = Contact(fullname= fake.name() , email = fake.ascii_free_email())

          result.save()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


channel.exchange_declare(exchange='task_service', exchange_type='direct')
channel.queue_declare(queue='task_campaing', durable=True)
channel.queue_bind(exchange='task_service', queue='task_campaing')


def main2():
    for i in range(1,30):
        task = Contact().save()
        channel.basic_publish(
            exchange='task_service',
            routing_key='task_campaing',
            body=str(task.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
    connection.close()


if __name__ == '__main__':
    main2()