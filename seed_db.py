import os
import json
from datetime import datetime
from faker import Faker

import model
import crud
import server

os.system('dropdb retame')
os.system('createdb retame')


fake = Faker()

model.connect_to_db(server.app)
model.db.create_all()


  

user_data = {}
for user in user_data: 
    user_data['user_name']= fake.user_name() 
    user_data['password']= fake.password() 
    user_data['email']= str(fake.email()) 


client_data = {}
for client in client_data: 
    client_data['fname']= fake.first_name() 
    client_data['lname']= fake.last_name() 
    client_data['email']= str(fake.email())




    with open('service_data/services.json') as f: 
        service_data = json.loads(f.read()) 

    
users_in_db = []
clients_in_db = []

for user in range(10):
    user_name = f'{fake.user_name()}'
    email = f'{fake.email()}'  
    password = f'{fake.password()}'

    user = crud.create_user(user_name, email, password)
    users_in_db.append(user)

    for client in range(10):
        fname = f'{fake.first_name()}'
        lname = f'{fake.last_name()}'
        email = f'{fake.email()}'

        client = crud.create_client(fname, lname, email)
        clients_in_db.append(client)

        

 