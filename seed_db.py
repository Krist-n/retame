import os
import json
from datetime import datetime
from faker import Faker
from random import randint

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

# Creating fake users
for user in range(10):
    user_name = fake.user_name()
    email = fake.email()
    password = fake.password()

    user = crud.create_user(user_name, email, password)
    users_in_db.append(user)

# Creating fake clients
    for client in range(10):
        fname = fake.first_name()
        lname = fake.last_name()
        email = fake.email()

        client = crud.create_client(fname, lname, email)
        clients_in_db.append(client)

# Creating fake Appointment records

ext_word_list = ['taper', 'fade', 'gradutation', 'sheers', 'theirs', 'sections', 'over direction', 'guard', \
    'razor', 'shave', 'use', 'comb', 'I', 'length', 'long', 'cut', 'my', 'shorten', 'low', 'sideburns', 'hairline', \
    '1', '2', '3', 'his', '4', '5', '6', 'make', '7', '8', 'thinned', 'he' 'texturized', 'softened', 'her', 'cowlick','thick', \
    'trimmers', 'natural', 'them', 'trim', 'section', 'elongate', 'lift', 'round', 'oval', 'wavy', 'curly', \
    'fine', 'coarse', 'angles', 'layers', 'bangs', 'elevation', 'look', 'shape', 'she', 'they', 'blowdry', 'them', 'thicken']

ext_word_list1 = ['shears', 'thinning shears', 'razor', 'straight blade', 'clippers', 'trimmers', 'texture shears']

fake.seed(0)
for appointment_rec in range(10):
    appt_date = f'{fake.datetime()}'
    service_notes = fake.paragraph(nb_sentence=3, ext_word_list)
    tools_used = fake.word(ext_word_list1)
    user_id = random.randint(1, 10)
    client_id = random.randint(1, 100)
    service_id = random.randint(1, 16)
    product_id = random.randint(1, 40)
    

        

 