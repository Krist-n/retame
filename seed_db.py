import os
import json
from datetime import datetime
import model
from faker import Faker

fake = Faker()



def input_data(x): 
  
    # dictionary 
    user_data ={} 
    for i in range(0, x): 
        user_data[i]['user_name']= fake.name() 
        user_data[i]['password']= fake.text() 
        user_data[i]['email']= str(f'{fake.text()}@test.com')
    print(user_data) 

    client_data ={} 
    for i in range(0, x): 
        client_data[i]['fname']= fake.name() 
        client_data[i]['lname']= fake.text() 
        client_data[i]['email']= str(f'{fake.text()}@test.com')
    print(client_data) 
  
    # # dictionary dumped as json in a json file 
    # with open('.json', 'w') as fp: 
    #     json.dump(user_data, fp)

    def main(): 
  
    # Enter number of clients and users 
        number_of_clients = 10
        number_of_users = 10 
        input_data(number_of_clients)
        input_data(number_of_users) 

# main() 