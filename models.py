
from mongoengine import *
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi 

uri = "mongodb+srv://nedwarov:<password>@cluster0.ti0rbne.mongodb.net/"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.homework9



 

class Authors(Document):
    fullname = StringField()
    born_date = StringField( )
    born_location = StringField( )
    description = StringField( )


class Quotes(Document):
    tags = ListField( )
    author =  ReferenceField (Authors)
    quotes = StringField ( )
    
class Contact(Document):
    fullname = StringField()
    email = EmailField()
    done = BooleanField(default=False)


      