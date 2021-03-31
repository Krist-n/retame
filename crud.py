"""CRUD operations."""

from model import db, User, Client, Appointment_rec, connect_to_db
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



if __name__ == '__main__':
    from server import app
    connect_to_db(app)
