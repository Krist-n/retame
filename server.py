from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
from datetime import date
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "top-secret"
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def homepage():
    """View homepage."""

    
    return render_template('index.html')



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

        session['current_logged_user']=user.user_id
        flash("Account created, please log in")

    return render_template('/index.html',
                            user=user.user_id, 
                            user_fname=user.fname,
                            user_lname=user.lname)

    return redirect('/')


@app.route('/select_or_add_client', methods=['POST'])
def login_user():
    """add and check for user login"""

    email = request.form['email']
    password = request.form['password']

    user = crud.get_user_by_email(email)
    clients = crud.get_all_clients()
   
   
    if user:
        if password == user.password:
            session['current_user_id'] = user.user_id
            session['current_user_fname'] = user.fname
            session['current_user_lname'] = user.lname
            
            print("**********************")
            print(f'logged in {user}')
            print("**********************")

            return render_template('add_or_select_client.html', 
                                    user=user, 
                                    clients=clients,
                                    current_user=user.user_id,
                                    user_fname=user.fname,
                                    user_lname=user.lname)
        else:
            flash("Incorrect password. Try again.")
            return redirect('/')
    flash("try again")
    return redirect('/') 


# @app.route('/users/<user_id>')
# def display_new_appointment_rec(user_id):
#     """Display appointment records for user"""

#     user = crud.get_user_by_user_id(user_id)

#     return render_template('appt_rec.html', user=user)

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


    if client:
        flash("This client already exists, try again.")
        return render_template("add_or_select_client.html")
    else:
        client = crud.create_client(fname, lname, email)
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
                                client_id=client.client_id, 
                                client_fname=client.fname,
                                client_lname=client.lname,
                                client_email=client.email,
                                user_fname=user.fname,
                                user_lname=user.lname)


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
    print(f"***       {client.client_id}              ***")
    print("**********************************************")

    user = crud.get_user_by_user_id(session['current_user_id'])
    session['current_user_id'] = user.user_id
    session['current_user_fname'] = user.fname
    session['current_user_lname'] = user.lname

# Client notes per section and perosnal

    back_panels = request.form.get('back_panels')
    tools_used = request.form.get('tools_used')
    right_panel = request.form.get('right_side')
    left_panel = request.form.get('left_side')
    top_panel = request.form.get('top_section')
    front_panel = request.form.get('front_section')
    personal_notes = request.form.get('personal_info')
    service_id = request.form.get('services')
    product_id = request.form.get('products')
    img_id = request.form.get('img')

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
                                                        img_id=img_id)

    
    print("*********************")
    print('new appointment record created')
    print("*********************")
#
    return render_template("/add_or_select_client.html",
                            user_id=user.user_id,
                            user_fname=user.fname,
                            user_lname=user.lname,
                            clients=clients)
    
# TODO     
# Services performed & tools used
    # service_performed = request.form.get('service_performed')

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

    print("***********************")
    print(f"{user.user_id}")
    print("***********************")


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
                         

    
 

@app.route('/users')
def get_users():    
    """Return all users"""

    users = crud.get_users()

    return render_template('all_users.html', users=users)


@app.route('/clients')
def get_client():    
    """Return a client"""

    client_id = request.args.get('client')

    print("*********************")
    print('client_id:', client_id)
    print("*********************")
    session['current_client_id'] = client_id


    return redirect(f'/clients/{client_id}')


@app.route('/services')
def get_all_services():    
    """Return all users"""

    services = crud.get_all_services()

    return render_template('all_services.html', services=services)


@app.route('/appointment_recs')
def get_appointment_recs():    
    """Return all appointment_recs"""

    appointment_recs = crud.get_all_appointment_recs()

    return render_template('all_appointment_recs.html', appointment_recs=appointment_recs)


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



            
     
           




if __name__ == '__main__':
    from model import connect_to_db 

    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

