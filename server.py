from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "top-secret"
app.jinja_env.undefined = StrictUndefined

@app.route('/schedule')
def schedule():
    """view schedulle"""
    user_name = request.form['email']
    password = request.form['password']

    return render_template('schedule.html')

@app.route('/services')
def all_services():    
    """getting all services"""

    services = crud.get_services()

    return render_template('all_services.html', services=services)



if __name__ == '__main__':
    from model import connect_to_db 

    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

