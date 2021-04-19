from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
from datetime import date
from random import choice
from collections import Counter
import requests
import crud
import os

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "Retame"
app.jinja_env.undefined = StrictUndefined


#<<< ------ Index route ------ >>>#

@app.route('/')
def homepage():
    """View homepage."""
    

    
    return render_template('index.html')


#<<< ------ Create an account for new user ------ >>>#

@app.route('/create_users', methods=['POST'])
def create_account():
    """create account"""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    # print(user)
    if user:
        return flash('A user already exists with that email.')
    else:
        user = crud.create_user(fname, lname, email, password)
        session['current_user_id'] = user.user_id
        session['current_user_fname'] = user.fname
        session['current_user_lname'] = user.lname

        print("***************")
        print(user.user_id)
        print("***************")

        session['current_user_id']=user.user_id
        flash("Account created, please log in")

        return redirect('/')
                            # user=user.user_id, 
                            # user_fname=user.fname,
                            # user_lname=user.lname)


#<<< ------ Check user password and login ------ >>>#
#<<< ------ Display clients both new and repeating ------ >>>#
#<<< ------ Select client for new appointment record ------ >>>#

@app.route('/select_or_add_client', methods=['GET', 'POST'])
def login_user():
    """add and check for user login"""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    clients = crud.get_all_clients()

    if user:
        if password == user.password:
            session['current_user_id'] = user.user_id
            session['current_user_fname'] = user.fname
            session['current_user_lname'] = user.lname
            session['current_user_email'] = user.email
            
            print("**********************")
            print(f'logged in {user}')
            print("**********************")
        else:
            flash("Incorrect password. Try again.")
            return redirect('/')

    client_list = set()
    new_clients = []
    
    # I want to pop remove all the clients that appear only once.
    
    
    clients_by_appt = crud.get_appointment_recs_by_user_id(session['current_user_id'])
    
    
    all_clients = set()
    repeating_clients = set()
    
    count = 0
    for recs in clients_by_appt:
        client = crud.get_client_by_client_id(recs.client_id)
        all_clients.add(client)
        print(all_clients)
        
        #if client is already in all_clients, that means they are a repeating client
        #if repeating client, we want to add to repeating_clients set
        #use set math, all clients minus repeating clients -> 
        if client in all_clients:   
            repeating_clients.add(client)
            

    new_clients = all_clients - repeating_clients
    # print(new_clients)
    
    num_new = len(new_clients)
    num_repeat = len(repeating_clients)
 


    return render_template('add_or_select_client.html', 
                            user=user, 
                            clients=clients,
                            user_clients=repeating_clients,
                            num_new=num_new,
                            num_reg=num_repeat,
                            new_clients=new_clients,
                            current_user=user.user_id,
                            user_fname=user.fname,
                            user_lname=user.lname)


#<<< ------ Logout user and redirect to index.html ------ >>>#

@app.route('/logout', methods=['POST'])
def log_out():
    """Log out current user, clear session."""

    session.clear()
    flash('You have been signed out.')

    print("************************")
    print("logged out user")
    print("************************")


    return redirect('/')

#<<< ------ Display user profile ------ >>>#
#<<< ------ Specify new and repeating customers ------ >>>#
#<<< ------ as well as the most & least consistent ------ >>>#

@app.route('/user_prof')
def render_user_prof():
    """display user profile"""
    

    counts = Counter()

    #appending client objs here
    users_clients = []
    new_clients = {}
    client_ids = []

    client_fname = []
    client_lname = []

    # we have num of visits for client in session but we need num visits for all clients the user has seen
    all_clients_visits = crud.get_appointment_recs_by_user_id(session['current_user_id'])
    for client in all_clients_visits:
        client = crud.get_client_by_client_id(client.client_id)
        client_ids.append(client.client_id)
        users_clients.append(client.fname + " " + client.lname)

        # appending client by fname and lname so I can undo my mess by using a dict counter 
        client_fname.append(client.fname)
        client_lname.append(client.lname)
    
    #zipping together fname and lname
    full_zip = zip(client_fname, client_lname)
    #turning it into a list so I can use it to query
    zipped_full_name = list(full_zip)
    #Using a set to ditch repeats
    fullnames_set = set(zipped_full_name)
    #Turning it back to a list
    fullname_list = list(fullnames_set)

    repeating_customer_email = []
    
    for names in fullname_list:
        fname = names[0]
        lname = names[1]
        email_new = crud.get_client_by_fname_and_lname(fname, lname)
        repeating_customer_email.append(email_new)

    # Example of fullname_list
    # [('Erica', 'Mcdonald'), ('Chuck', 'Brown'), ('Hazard', 'Danger'), ('Michael', 'Villarreal')]

    #getting a tally of all appointments created for each user
    #making it a dictionary for easier accessibility
    visits_dict = dict(Counter(users_clients))
    print(visits_dict)
    #created func to filter out clients that visited only once
    def find_clients_with_least_visits(clients):
        """finding clients with only 1 visit"""
        return visits_dict[clients] < 2
   
    # utilizing earlier function and getting all new clients    
    new_clients = list(filter(find_clients_with_least_visits, visits_dict.keys()))
    num_new = len(new_clients)

    split_new = []
    for client in new_clients:
        split_new.append(client.split(" "))
    
    new_client_email = []
    for client in split_new:
        fname = client[0]
        lname =  client[1]
        email_new = crud.get_client_by_fname_and_lname(fname, lname)
        new_client_email.append(email_new)

    email_client = []
    for email in new_client_email:
        for client in email:
            c_email = client.email.split(" ")
            for e in c_email:
                print(e)
                email_client.append(e)
         

    # getting the client with the most visits to display to page
    max_key = max(visits_dict, key=visits_dict.get)

    
    # clearing out new clients to display repeating clients only
    for key, value in list(visits_dict.items()):
        if value < 2:
            del visits_dict[key]
    
    user = crud.get_user_by_user_id(session['current_user_id'])
    session['current_user_id'] = user.user_id
    session['current_user_fname'] = user.fname
    session['current_user_lname'] = user.lname

    return render_template('user_profile.html',
                            max_key=max_key,
                            num_new=num_new,
                            visits_dict=visits_dict,
                            new_clients=new_clients,
                            email=email_client,
                            fname=user.fname,
                            lname=user.lname)

#<<< ------ Create and add new client to the session and db ------ >>>#

@app.route('/create_client', methods=['POST'])
def add_new_client():
    """add new client to db"""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')


    client = crud.get_client_by_email(email)
   
    user = crud.get_user_by_user_id(session['current_user_id'])
    session['current_user_id'] = user.user_id
    session['current_user_fname'] = user.fname
    session['current_user_lname'] = user.lname

    services = crud.get_all_services()
    products = crud.get_all_products()

    new_clients = []
    num_new = len(new_clients)
    
    if client:
        flash("This client already exists, try again.")
        return render_template("add_or_select_client.html")
    else:
        client = crud.create_client(fname, lname, email)
        new_clients.append(client)
# create client - append to new
        session['current_client_id'] = client.client_id
        session['current_client_fname'] = client.fname
        session['current_client_lname'] = client.lname
        session['current_client_email'] = client.email


        print("*********************")
        print(f'created new client: {client}')
        print("*********************")

        


        

        return render_template('new_service_notes.html', 
                                client=client.email,
                                services=services,
                                products=products,
                                new_clients=new_clients,
                                num_new=num_new,
                                client_id=client.client_id, 
                                client_fname=client.fname,
                                client_lname=client.lname,
                                client_email=client.email,
                                user_fname=user.fname,
                                user_lname=user.lname)



#<<< ------ Form for appointments for each client ------ >>>#

@app.route("/create_new_appointment_rec", methods=['POST'])
def create_new_appointment():
    """Showing new appointment form"""


    appt_date = request.form.get('date')

    print("**************")
    print(appt_date)
    print("**************")

    #  send all clients to the add_or_select_client.html
    clients = crud.get_all_clients()

    client = crud.get_client_by_client_id(session['current_client_id'])
    session['current_client_id'] = client.client_id
    session['current_client_fname'] = client.fname
    session['current_client_lname'] = client.lname

    print("**********************************************")
    print(f"***  client first name:   {client.fname}  ***")
    print("**********************************************")

    user = crud.get_user_by_user_id(session['current_user_id'])
    session['current_user_id'] = user.user_id
    session['current_user_fname'] = user.fname
    session['current_user_lname'] = user.lname

# Client notes per section and perosnal

    back_panels = request.form.get('back_panels')
    right_panel = request.form.get('right_side')
    left_panel = request.form.get('left_side')
    top_panel = request.form.get('top_section')
    front_panel = request.form.get('front_section')
    personal_notes = request.form.get('personal_info')
    tools_used = request.form.get('tools_used')
    service_id = request.form.get('services')
    product_id = request.form.get('products')
    img_path = None
    img_id = None
   

    client_list = set()
    new_clients = []
    
    # I want to pop remove all the clients that appear only once.
    
    
    clients_by_appt = crud.get_appointment_recs_by_user_id(session['current_user_id'])
    
    
    all_clients = set()
    repeating_clients = set()
    # print("<---------------------------------------->")
    for recs in clients_by_appt:
        client = crud.get_client_by_client_id(recs.client_id)
        print(client.client_id)
        
        
        #if client is already in all_clients, that means they are a repeating client
        #if repeating client, we want to add to repeating_clients set
        #use set math all clients minus repeating clients -> 
        if client in all_clients:
            repeating_clients.add(client)
        
        all_clients.add(client)
        
    new_clients = all_clients - repeating_clients
    
    num_new = len(new_clients)
    num_repeat = len(repeating_clients)
    # print("*******************")
    # print(num_repeat)

    ALLOWED_EXTENSIONS = {'gif', 'png', 'jpg', 'jpeg'}

    def allowed_file(filename):
        """Return file with allowed extensions."""

        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    def upload_img_file():
        """upload appointment img"""

        file = request.files['img_path']
        
        result = requests.post('cloudinary.uploader.unsigned_upload(file, upload_preset, **options)')    
        


        

    new_appointment_rec = crud.create_appointment_rec(appt_date=appt_date, 
                                                        tools_used=tools_used,
                                                        back_panels=back_panels,
                                                        right_panel=right_panel,
                                                        left_panel=left_panel,
                                                        top_panel=top_panel,
                                                        front_panel=front_panel,
                                                        personal_notes=personal_notes,
                                                        user_id=user.user_id,
                                                        client_id=client.client_id,
                                                        service_id=service_id, 
                                                        product_id=product_id,
                                                        img_path=img_path,
                                                        img_id=img_id)

    
    print("*********************")
    print('new appointment record created')
    print("*********************")
    
    return render_template("/add_or_select_client.html",
                            user_id=user.user_id,
                            user_clients=repeating_clients,
                            user_fname=user.fname,
                            user_lname=user.lname,
                            clients=clients,
                            new_clients=new_clients,
                            num_new=num_new,
                            num_reg=num_repeat)
    

#<<< ------ after creating new client render new_service_notes.html ------ >>>#
#<<< ------ keep current session in flow ------ >>>#

@app.route("/add_new_rec")
def move_to_create_appointment():
    """display new appointment record to be filled in"""


    print("***********************")
    print("went to new form")
    print("***********************")
    
    services = crud.get_all_services()
    products = crud.get_all_products()

    client = crud.get_client_by_client_id(session['current_client_id'])
    session['current_client_id'] = client.client_id
    session['current_client_fname'] = client.fname
    session['current_client_lname'] = client.lname

    print("***********************")
    print(f"{client.fname}")
    print("***********************")


    user = crud.get_user_by_user_id(session['current_user_id'])
    session['current_user_id'] = user.user_id
    session['current_user_fname'] = user.fname
    session['current_user_lname'] = user.lname

    return render_template('new_service_notes.html',
                            services=services,
                            products=products,
                            client=client,
                            client_id=client.client_id,
                            client_fname=client.fname,
                            client_lname=client.lname,
                            user=user.user_id,
                            user_fname=user.fname,
                            user_lname=user.lname)
                         
#<<< ------ Get all users ------ >>>#

@app.route('/users')
def get_users():    
    """Return all users"""

    users = crud.get_users()

    return render_template('all_users.html', users=users)


#<<< ------ get all clients ------ >>>#

@app.route('/clients')
def get_client():    
    """Return a client"""

    client_id = request.args.get('client')

    session['current_client_id'] = client_id


    return redirect(f'/clients/{client_id}')

#<<< ------ get all services ------ >>>#

@app.route('/services')
def get_all_services():    
    """Return all users"""

    services = crud.get_all_services()

    return render_template('all_services.html', services=services)

#<<< ------ get all appointment records ------ >>>#

@app.route('/appointment_recs')
def get_appointment_recs():    
    """Return all appointment_recs"""

    appointment_recs = crud.get_all_appointment_recs()

    return render_template('all_appointment_recs.html', appointment_recs=appointment_recs)

#<<< ------ Display a clients details from previous records ------ >>>#

@app.route('/clients/<client_id>')
def show_client(client_id):
    """Show details on a particular client."""

    user = crud.get_user_by_user_id(session['current_user_id'])
    session['current_user_id'] = user.user_id
    session['current_user_fname'] = user.fname
    session['current_user_lname'] = user.lname

    client = crud.get_client_by_client_id(session['current_client_id'])
    session['current_client_id'] = client.client_id
    session['current_client_fname'] = client.fname
    session['current_client_lname'] = client.lname
    session['current_client_email'] = client.email
    

    return render_template('client_details.html',
                            client=client, 
                            client_id=client.client_id,
                            client_fname=client.fname,
                            client_lname=client.lname,
                            client_email=client.email,
                            user_id=user.user_id,
                            user_fname=user.fname,
                            user_lname=user.lname)

#<<< ------ Get all clients seen by the user in session ------ >>>#

@app.route('/clients_seen_by_user')
def show_all_clients_by_user_id():
    """show all new and repeat clients for user in session"""

    user_clients = []
    all_clients = set()
    repeating_clients = set()

    appt_recs = crud.get_appointment_recs_by_user_id(session['current_user_id'])

    for records in appt_recs:
        user_clients.append(records.client_id)
        print(f'******** appt records for user: {records.client_id} ********')

    for client in appt_recs:
        if client in all_clients:
            repeating_clients.add(client)
        
        all_clients.add(client)
        
    new_clients = all_clients - repeating_clients

    num_new = len(new_clients)
    num_repeat = len(repeating_clients)

    return render_template('add_or_select_client.html',
                            num_new=num_new,
                            num_reg=num_repeat, 
                            user_clients=user_clients)
   
  



            
     
           




if __name__ == '__main__':
    from model import connect_to_db 

    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)




# Counting how many visits a specific client has made (with a specific stylist)
# Query appt recs table and filter by client id & user id -> list of appt recs
# calculate the length of that list -> number of visits