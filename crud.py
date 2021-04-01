"""CRUD operations."""

from model import db, User, Client, Appointment_rec, Service, connect_to_db
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
    """return a list of all users"""
    
    return Service.query.filter(Service.service_name == service_name).first()

    

if __name__ == '__main__':
    from server import app

    connect_to_db(app)
