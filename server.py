from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "top-secret"
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def homepage():
    """View homepage."""


    return render_template('homepage.html')



@app.route('/users', methods=['POST'])
def create_account():
    """create account"""

    print("HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    print(user)
    if user:
        return flash('A user already exists with that email.')
    else:
        crud.create_user(fname, lname, email, password)
        flash("Account created, please log in")

    return redirect('/')


@app.route('/login', methods=['POST'])
def login_user():
    """add and check for user login"""

    email = request.form['email']
    password = request.form['password']

    user = crud.get_user_by_email(email)
    if user:
        if password == user.password:
            flash("You've logged in!")
            return redirect('/')
        else:
            flash("Incorrect password. Try again.")
            return redirect('/')
 

@app.route('/users')
def get_users():    
    """Return all users"""

    users = crud.get_users()

    return render_template('all_users.html', users=users)

@app.route('/clients')
def get_all_clients():    
    """Return all users"""

    clients = crud.get_all_clients()

    return render_template('all_clients.html', clients=clients)


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

    client = crud.get_client_by_client_id(client_id)
   

    return render_template('client_details.html', client=client)



if __name__ == '__main__':
    from model import connect_to_db 

    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

