from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, Client
from datetime import date
from random import choice
from collections import Counter
import requests
import crud
import os
import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api


from jinja2 import StrictUndefined

app = Flask(__name__)

app.config['CLOUDINARY_UPLOAD_API_URL'] = "https://api.cloudinary.com/v1_1/retame/image/upload"
app.secret_key = "Retame"

app.jinja_env.undefined = StrictUndefined


#<<< ------ Index route ------ >>>#

@app.route('/')
def index():
    """display index page"""
    

    return render_template('index.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """add and check for user login"""
    

    print("log in route -----------------------")
    # Pull user info from form
    email = request.form.get('email')
    password = request.form.get('password')

    # Get user by email and check password
    user = crud.get_user_by_email(email)

    print(f'--------{email}-----------')

    if user:
        print(f'-------- password={password} - user.password={user.password} -----------')
        if password == user.password:
            session['logout'] = False
            session['current_user_id'] = user.user_id
            session['current_user_fname'] = user.fname
            session['current_user_lname'] = user.lname
            session['current_user_email'] = user.email
            
            print("**********************")
            print(f'logged in {user}')
            print("**********************")

            return redirect('/user_homepage')
        
        else:
            session['login_attempt'] = True
            return redirect('/')
    else:
        session['login_attempt'] = True
        return redirect('/')
######################## - Toast Routes - ########################
@app.route('/isloggedin')
def logged_in():
    """Logged in Toast notification"""

    print("*******************************ISLOGGEDIN")

    if 'current_user_email' in session and 'current_client_id' not in session:
        user = crud.get_user_by_email(session['current_user_email'])
        
        return f"{user.fname} {user.lname} logged in!"
    else:
        return None

###########################################################################
@app.route('/attempted_login')
def attempted_login():
    """Login attempt Toast notification"""

    if session['login_attempt'] == True:
        print("HIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        return "Incorrect email or password, please try again"
    elif session['logout'] == True:
        return redirect("/")

        

            
###########################################################################
@app.route('/appointment_created')
def appointment_created():
    """toast route for appointment saved confirmation"""

    if 'current_client_id' in session:
        client = crud.get_client_by_client_id(session['current_client_id'])
        return f"New appointment for {client.fname} {client.lname} created!"

    else:
        return redirect('/user_homepage')

###########################################################################
@app.route('/logout_user')
def logout_user():
    """Toast route for logging out"""

    goodbye = ['in awhile crocodile', 'see you later alligator', 'peace out cub scout', \
    'gotta go, buffalo', 'Adieu, cockatoo!', 'Live long and prosper']

    
    if session['logout'] == True:
        return choice(goodbye)

###########################################################################
#<<< ------ Logout user and redirect to index.html ------ >>>#

@app.route('/logout', methods=['POST'])
def log_out():
    """Log out current user, clear session."""

    print("************************")
    print("logged out user")
    print("************************")

    session.clear()
    session['logout'] = True

    return redirect('/')


#<<< ------ Create an account for new user ------ >>>#

@app.route('/create_users', methods=['POST'])
def create_account():
    """create account"""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    
    if user:
        return "A user already exists with that email."
    else:
        user = crud.create_user(fname, lname, email, password)

        print("***************")
        print(user.user_id)
        print("***************")

        session['current_user_id']=user.user_id
        return "Account created, please log in"


#<<< ------ Check user password and login ------ >>>#
#<<< ------ Display clients both new and repeating ------ >>>#
#<<< ------ Select client for new appointment record ------ >>>#

@app.route('/user_homepage', methods=['GET', 'POST'])
def user_homepage():
    """Display user homepage after log in"""

    if 'current_user_id' not in session:
        return redirect("/")
    
    user = crud.get_user_by_user_id(session['current_user_id'])
       

    # Get all clients
    all_clients = crud.get_all_clients()
    
    # Get all appnt recs for this user
    appnt_recs_by_user = crud.get_appointment_recs_by_user_id(user.user_id)
    
    clients_by_appnt = []
    repeating_clients = []
    new_clients = []

    for recs in appnt_recs_by_user:
        # Get the client for this record and append to clients by appnt list
        client = crud.get_client_by_client_id(recs.client_id)
        clients_by_appnt.append(client)
        
        # If client is repeating, put in repeating clients list 
        if client in new_clients:   
            repeating_clients.append(client)
        else:
            new_clients.append(client)

    # Removing repeating ids in repeating_clients to list regulars          
    repeating_clients = set(repeating_clients)
    new_clients = set(new_clients)

    # Separate out new clients from repeating
    new_clients = new_clients - repeating_clients

    # Get number of repeating and new clients
    num_new = len(new_clients)
    num_repeat = len(repeating_clients)

    print("...............................................................")
    print(all_clients)

    return render_template('user_homepage.html', 
                            user=user, 
                            clients=all_clients,
                            user_clients=repeating_clients,
                            num_new=num_new,
                            num_reg=num_repeat,
                            new_clients=new_clients)



#<<< ------ Display user profile ------ >>>#
#<<< ------ Specify new and repeating customers ------ >>>#
#<<< ------ as well as the most & least consistent ------ >>>#

@app.route('/user_prof')
def render_user_prof():
    """display user profile"""

    user = crud.get_user_by_user_id(session['current_user_id'])
    appnt_recs_by_user = crud.get_appointment_recs_by_user_id(user.user_id)

    repeating_clients = []
    new_clients = []

    for recs in appnt_recs_by_user:
        # Get the client for this record and append to clients by appnt list
        client = crud.get_client_by_client_id(recs.client_id)
        
        # If client is repeating, put in repeating clients list 
        if client in new_clients:   
            repeating_clients.append(client)
        else:
            new_clients.append(client)
    
    repeating_clients = set(repeating_clients)

    new_clients = set(new_clients)
    
    users_clients = []
 
    client_fname = []
    client_lname = []

    # parsing through appointment records table and querying by client obj
    for appnt_rec in appnt_recs_by_user:
        # getting all client obj by user id
        client = crud.get_client_by_client_id(appnt_rec.client_id)
        # adding clients full name to users_clients for html formatting
        users_clients.append(client.fname + " " + client.lname)

        # appending client by fname and lname so I can query for both fname & lname
        client_fname.append(client.fname)
        client_lname.append(client.lname)

    #zipping together (creates tuples), fname & lname for accurate alignment of fullname
    full_zip = zip(client_fname, client_lname)
    #turning it into a list so I can use it to query
    zipped_full_name = list(full_zip)
    #Using a set to remove repeats
    fullnames_set = set(zipped_full_name)
    #Turning it back to a list for indexing on line 225
    fullname_list = list(fullnames_set)
    
    # Looping through and indexing the fullname_list to grab first and last names for query args
    for names in fullname_list:
        fname = names[0]
        lname = names[1]
      
    #getting a tally of all appointments created for each client by user
    #making it a dictionary for easier accessibility
    visits_dict = dict(Counter(users_clients))

    #created func to filter out clients that visited only once
    def find_clients_with_least_visits(clients):
        """finding clients with only 1 visit"""
        return visits_dict[clients] < 2
   
    # utilizing earlier function and getting all new clients 
    # Storing number of new clients for html display   
    new_clients = list(filter(find_clients_with_least_visits, visits_dict.keys()))
    num_new = len(new_clients)

    # splitting clients to seperate out first and last name for querying
    split_new_clients = []
    for client in new_clients:
        split_new_clients.append(client.split(" "))
    
    # at last querying by fname and lname for new clients email
    new_client_email = []
    for client in split_new_clients:
        fname = client[0]
        lname =  client[1]
        email_new = crud.get_client_by_fname_and_lname(fname, lname)
        new_client_email.append(email_new)

    # Nested for loops : "There be dragons"
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


    return render_template('user_profile.html',
                            max_key=max_key,
                            num_new=num_new,
                            visits_dict=visits_dict,
                            new_clients=new_clients,
                            email=email_client,
                            user=user)

#<<< ------ Create and add new client to the session and db ------ >>>#

@app.route('/create_client', methods=['POST'])
def add_new_client():
    """add new client to db"""

    # Getting client information to add client to db
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')

    # Checking to see if client is in the db
    client = crud.get_client_by_email(email)
    if client:
        flash("Client already exists")
    else:
        flash("New client created.")
        client = crud.create_client(fname, lname, email)
        

        print("*********************")
        print(f'created new client: {client}')
        print("*********************")
    
        return redirect('/user_homepage')

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

    print("**********************************************")
    print(f"***  client first name:   {client.fname}  ***")
    print("**********************************************")

    user = crud.get_user_by_user_id(session['current_user_id'])

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
    img_path = request.form.get('inputGroupFile04')
   
    file = request.files['file']

    upload_img_file = cloudinary.uploader.unsigned_upload(file, "kuxl99l1", cloud_name='retame')
    print('upload_img_file:')
    print(upload_img_file)

    img_path = upload_img_file['secure_url']
    
    appt_img = crud.create_appt_img(upload_img_file['secure_url'], appt_date)
    img_id = appt_img.img_id

       
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
    
    print("**********************************************")
    print(img_path)
    print("**********************************************")
    print('new appointment record created')
    print("**********************************************")

    return redirect('/user_homepage')



@app.route('/create_img')
def add_appointment_imgs():
    """Add users imgs""" 

    ALLOWED_EXTENSIONS = {'gif', 'png', 'jpg', 'jpeg'}

    def allowed_file(filename):
        """Return file with allowed extensions."""

        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    def upload_img_file():
        """upload appointment img"""

        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('file type not allowed')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                upload_img_file = cloudinary.uploader.unsigned_upload(file, "kuxl99l1", folder = 'retame')
                print('upload_img_file:')
                print(upload_img_file)
        
                img_path = upload_img_file['secure_url']

    return redirect('/create_new_appointment_rec')  

#<<< ------ after creating new client render new_service_notes.html ------ >>>#
#<<< ------ keep current session in flow ------ >>>#

@app.route("/add_new_rec")
def move_to_create_appointment():
    """display new appointment record to be filled in"""
    
    services = crud.get_all_services()
    products = crud.get_all_products()
    client = crud.get_client_by_client_id(session['current_client_id'])
    user = crud.get_user_by_user_id(session['current_user_id'])
    

    return render_template('service-notes-base.html',
                            services=services,
                            products=products,
                            client=client,
                            user=user)
                         
#<<< ------ Get all users ------ >>>#

@app.route('/users')
def show_users():    
    """Return all users"""

    users = crud.get_users()

    return render_template('all_users.html', users=users)


#<<< ------ get all clients ------ >>>#

@app.route('/clients')
def get_client():    
    """Return a client"""

    client_id = request.args.get('client')
    print(request.args)
    session['current_client_id'] = client_id
    
    return redirect(f'/clients/{client_id}')

#<<< ------ get all services ------ >>>#

@app.route('/services')
def show_all_services():    
    """Return all users"""

    services = crud.get_all_services()

    return render_template('all_services.html', services=services)

#<<< ------ get all appointment records ------ >>>#

@app.route('/appointment_recs')
def show_appointment_recs():    
    """Return all appointment_recs"""

    appointment_recs = crud.get_all_appointment_recs()

    return render_template('all_appointment_recs.html', appointment_recs=appointment_recs)

#<<< ------ Display a clients details from previous records ------ >>>#

# @app.route('/search')
# def search_clients():
#     """Search form"""

#     # getting input from user search
#     client_name = request.args.get("search")
#     # creating a first name and last name ele
#     client_query_str = client_name.split(" ")
#     # db search by first and last name
#     fullname = crud.get_client_by_fname_and_lname(client_query_str[0], client_query_str[1]) 
    
#     print(client_query_str)

#     for name in fullname:
#         search_results = name
        
#     return redirect('/user_homepage')

@app.route('/clients/<client_id>')
def show_client(client_id):
    """Show details on a particular client."""
    
    # session['current_client_id'] = client_id

    user = crud.get_user_by_user_id(session['current_user_id'])
    client = crud.get_client_by_client_id(session['current_client_id'])
    appts = crud.get_appointment_recs_by_client_id(session['current_client_id'])

    all_user_img_paths = []

    if appts:
        for record in appts:
            if record.img_path != None:
                img_path = record.img_path
           
                all_user_img_paths.append(img_path)
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print(img_path)
            else:
                img_path = None
             
    else:
        img_path = None
    return render_template('client_details.html',
                                        client=client, 
                                        user=user,
                                        img_path=img_path)
   
  



if __name__ == '__main__':
    from model import connect_to_db 

    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

