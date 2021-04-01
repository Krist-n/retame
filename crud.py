"""CRUD operations."""

from model import db, User, Client, Appointment_rec, Service, Product, connect_to_db
from datetime import datetime
from faker import Faker

fake = Faker()

def create_user(user_name, email, password):
    """Create and return a new user."""

    user = User(user_name=user_name, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_client(fname, lname, email):
    """Create and return a new client."""

    client = Client(fname=fname, lname=lname, email=email)

    db.session.add(client)
    db.session.commit()

    return client

def create_service(service_name, description, price):
    """Create and return a new service"""

    service = Service(service_name=service_name, description=description, price=price)

    db.session.add(service)
    db.session.commit()

    return service

def get_users():
    """return a list of all users"""
    
    return User.query.all()

def get_user_by_email(email):
    """get user by email"""

    return User.query.filter(User.email == email).first()

def get_user_by_user_name(user_name):
    """get user by user_name"""

    return User.query.filter(User.user_name == user_name).first()

def get_client():
    """return a list of all clients"""
    
    return Client.query.all()

def get_client_by_email(email):
    """get client by email"""

    return Client.query.filter(Client.email == email).first()

def get_services():
    """return a list of all services"""
    
    return Service.query.all()

def get_services_by_name(service_name):
    """return a service"""
    
    return Service.query.filter(Service.service_name == service_name).first()

def create_appointment_rec(user_id, client_id, appt_date, service_notes, tools_used):
    """creating appointment records"""

    appointment_rec = Appointment_rec(user_id=user_id, client_id=client_id, appt_date=appt_date, service_notes=service_notes, tools_used=tools_used)

    db.session.add(appointment_rec)
    db.commit()

    return appointment_rec

def get_appointment_recs():
    """return a list of all appointment recs"""

    return Appointment_rec.query.all()

def get_appointment_recs_by_user_id(user_id):
    """return a list of all appointment records for specific user_id"""

    return Appointment_rec.query.filter(Appointment_rec.user_id == user_id).all()

def get_appointment_recs_by_client_id(client_id):
     """return a list of all appointment records for specific client_id"""

     return Appointment_rec.query.filter(Appointment_rec.client_id == client_id).all()

def get_appointment_recs_by_date(appt_date):
    """return a list of all appointment records for specific date"""

    return Appointment_rec.query.filter(Appointment_rec.appt_date == appt_date).all()

def get_appointment_recs_by_appt_rec_id(appt_rec_id):
    """Return appointment record with this appt_rec_id"""

    return Appointment_rec.query.filter(Appointment_rec.appt_rec_id == appt_rec_id).first()

def get_appointment_recs_by_product_id(product_id):
    """Return a list of all appointment_recs with this product id."""

    return Appointment_rec.query.filter(Appointment_rec.product_id == product_id).all()

def get_appointment_recs_by_tools_used(tools_used, tool):
    """Return a list of all appointment recs with this tool used"""
    
    for tool in tools_used:
        if tool in tools_used:
            return Appointment_rec.query.filter(Appointment_rec.tools_used == tool).all()

def create_product(product_name, product_categories, price):
    """create and return a new product"""

    product = product_name=product_name, product_categories=product_categories, price=price

    db.session.add(product)
    db.session.commit()

def get_product_by_id(product_id):
    """return product by id"""

    return Product.query.filter(Product.product_id == product_id).first()

def get_product_by_name(product_name):
    """return product by name"""

    return Product.query.filter(Product.product_name == product_name).first()

def get_product_by_product_categories(product_categories):
    """return a list of all products in the category"""

    return Product.query(Product.product_categories == product_categories).all()




    

if __name__ == '__main__':
    from server import app

    connect_to_db(app)
