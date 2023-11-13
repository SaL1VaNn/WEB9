import json
from models import *
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import * 
from prod import main2, maker_contacts
from consumer import channel
from main import start_pars_process

connect(
    db='homework9',
    host='mongodb+srv://nedwarov:<password>@cluster0.ti0rbne.mongodb.net/',
    )

if __name__ == '__main__':
   
     while  True:
       a= 'enter "6" for start RabbitMQ (id contakt) send to emeil'
       b= 'enter "5" start generate contacts for db '
       c = 'enter "1" For start Scrapy process on need url  '
       d = '----------------------------------------------------'
       menu = input (f' {d}\n {c}\n enter "2" for load db from json file\n enter "3" if you want to find quotes by author\n enter "4" if you want to find quotes by tags\n {b}\n {a}\n enter "exit" or "7" to quiet : ')
       
       if menu == 'exit' or menu == '7':
           print("Good bye!")
           break
       elif menu == '2':
            with open('authors.json', "r", encoding='utf-8') as f:
                data = json.load(f)
                for author in data:
                    result = Authors(fullname=author['fullname'], born_date=author['born_date'],
                            born_location=author['born_location'], description=author['description'])
                    result.save()

            with open('quotes.json', "r", encoding='utf-8') as f:
                data = json.load(f)
                for quote in data:                        
                    result = Quotes(tags=quote['tags'], author=Authors.objects.get(fullname=quote['author']),  
                                    quotes=quote['quote'])
                    result.save()
            print (' ok')     

       elif menu == "3":
           name =  input('author: ') 
           i = Authors.objects.get( fullname = f"{name}" )
           print (f'{i.description}' )
         
       elif menu == '4' : 
            tags = input('enter tags no spaces separated by commas : ')  
            j =  Quotes.objects.get( tags= f'{tags}' )
            print(f'{j.quotes }' )
       elif menu == '5' : 
           maker_contacts()

       elif menu == '6' : 
           main2()
           channel.start_consuming()
       elif menu == '1' : 
           start_pars_process()
        
       else : print( 'unknown command, try again' )
 
