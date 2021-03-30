import os
import json
from datetime import datetime
from faker import Faker

import model
import server

os.system('dropdb retame')
os.system('createdb retame')


fake = Faker()

model.connect_to_db(server.app)
model.db.create_all()

def input_data(x): 
  
    # dictionary 
    user_data ={} 
    for user in user_data: 
        user_data['user_name']= fake.user_name() 
        user_data['password']= fake.password() 
        user_data['email']= str(fake.email())
    print(user_data) 

    client_data ={} 
    for client in client_data: 
        client_data['fname']= fake.first_name() 
        client_data['lname']= fake.last_name() 
        client_data['email']= str(fake.email())
    print(client_data) 
   
    def main(): 
  
    # Enter number of clients and users 
        number_of_clients = 10
        number_of_users = 10 
        input_data(number_of_clients)
        input_data(number_of_users) 

 