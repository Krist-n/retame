import os
import json
from random import randint, choice
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



users_in_db = []
clients_in_db = []

# Creating fake users
for user in range(10):
    fname = fake.first_name()
    lname = fake.last_name()
    email = fake.email()
    password = fake.password()

    user = crud.create_user(fname, lname, email, password)
    users_in_db.append(user)

# Creating fake clients
for client in range(10):
    fname = fake.first_name()
    lname = fake.last_name()
    email = fake.email()

    client = crud.create_client(fname, lname, email)
    clients_in_db.append(client)

# Parsing through json service_date
with open('data/service_data.json') as f: 
        service_data = json.loads(f.read())

for service in service_data:
    service_name, description, price = (service['service_name'],
                                        service['description'],
                                        service['price']) 

    db_service = crud.create_service(service_name,
                                    description,
                                    price)

# Parsing through json product_date
with open('data/product_data.json') as f: 
        product_data = json.loads(f.read())

for product in product_data:
    product_name, product_category, price = (product['product_name'],
                                            product['product_category'],
                                            product['price']) 

    db_product = crud.create_product(product_name,
                                    product_category,
                                    price)

# Creating images file for random img 
path = '/home/vagrant/src/project/static/img'
appt_img = choice([x for x in os.listdir(path) 
                            if os.path.isfile(os.path.join(path, x))])
                          
for img in range(10):
    img_path = appt_img
    img_date = fake.past_datetime()

    db_appt_img = crud.create_appt_img(img_path, img_date)


# Creating fake Appointment records
service_notes_word_list = ['taper', 'fade', 'gradutation', 'sheers', 'theirs', 'sections', 'over direction', 'guard', \
    'razor', 'shave', 'use', 'comb', 'I', 'length', 'long', 'cut', 'my', 'shorten', 'low', 'sideburns', 'hairline', 
    '1', '2', '3', 'his', '4', '5', '6', 'make', '7', '8','when', 'with' 'thinned', 'he' 'texturized', 'softened', 'her', 
    'cowlick','thick', 'trimmers', 'natural', 'them', 'trim', 'section', 'elongate', 'lift', 'round', 'oval', 'wavy', 'curly', 
    'fine', 'coarse', 'angles', 'layers', 'bangs', 'was', 'elevation', 'look', 'shape', 'she', 'they', 'blowdry', 'them', 'thicken']


tools_used_word_list = ['shears', 'thinning shears', 'razor', 'straight blade', 'clippers', 'trimmers', 'texture shears']

appt_rec_in_db = []

random_past_date = fake.past_datetime()


with open('data/appointment_rec_data.json') as f: 
        appointment_data = json.loads(f.read())

Faker.seed(0)
for record in appointment_data:
    record['appt_date'] = fake.past_datetime()
    appt_date = record['appt_date']
    record['back_panels'] = fake.paragraph(nb_sentences=3, ext_word_list=service_notes_word_list)
    back_panels = record['back_panels']
    record['right_panel'] = fake.paragraph(nb_sentences=3, ext_word_list=service_notes_word_list)
    right_panel = record['right_panel']
    record['left_panel'] = fake.paragraph(nb_sentences=3, ext_word_list=service_notes_word_list)
    left_panel = record['left_panel']
    record['top_panel'] = fake.paragraph(nb_sentences=3, ext_word_list=service_notes_word_list)
    top_panel = record['top_panel']
    record['front_panel'] = fake.paragraph(nb_sentences=3, ext_word_list=service_notes_word_list)
    front_panel = record['front_panel']
    record['personal_notes'] = fake.paragraph(nb_sentences=3, ext_word_list=service_notes_word_list)
    personal_notes = record['personal_notes'] 
    record['tools_used'] = fake.word(ext_word_list=tools_used_word_list)
    tools_used = record['tools_used']
    user_id, client_id, service_id, product_id, img_path, img_id = (record['user_id'],
                                                        record['client_id'],
                                                        record['service_id'],
                                                        record['product_id'],
                                                        record['img_path'],
                                                        record['img_id'])

    appt_rec_in_db.append(appointment_data)
    appt_rec = crud.create_appointment_rec(appt_date, back_panels, right_panel, \
    left_panel, top_panel, front_panel, personal_notes, tools_used, user_id, client_id, \
    service_id, product_id, img_path, img_id)



        

 