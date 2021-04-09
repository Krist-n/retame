"""CRUD operations."""

from model import db, User, Client, Appointment_rec, Service, Product, Appt_img, connect_to_db
from datetime import datetime
from faker import Faker

fake = Faker()


#<<< ------ Creating data ------ >>>#

def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password)

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


def create_appointment_rec(appt_date, back_panels, right_panel, left_panel, \
    top_panel, front_panel, personal_notes, tools_used, user_id, client_id, service_id,\
     product_id, img_id):
    """creating appointment records"""

    appointment_rec = Appointment_rec(appt_date=appt_date, back_panels=back_panels, \
        right_panel=right_panel, left_panel=left_panel, \
        top_panel=top_panel, front_panel=front_panel, personal_notes=personal_notes, \
        tools_used=tools_used, user_id=user_id, client_id=client_id, service_id=service_id,\
        product_id=product_id, img_id=img_id)

    db.session.add(appointment_rec)
    db.session.commit()

    return appointment_rec


def create_appt_img(url, img_date):
    """create and return an appointment image"""

    appt_img = Appt_img(url=url, img_date=img_date)

    db.session.add(appt_img)
    db.session.commit()

    return appt_img


def create_product(product_name, product_category, price):
    """create and return a new product"""

    product = Product(product_name=product_name, product_category=product_category, price=price)

    db.session.add(product)
    db.session.commit() 

    return product  


#<<< ------ User queries ------ >>>#

def get_users():
    """return a list of all users"""
    
    return User.query.all()


def get_user_by_user_id(user_id):
    """get user by user_name"""

    return User.query.filter(User.user_id == user_id).first()


def get_user_by_fname(fname):
    """get user by user_name"""

    return User.query.filter(User.fname == fname).first()


def get_user_by_lname(lname):
    """get user by user_name"""

    return User.query.filter(User.lname == lname).first()


def get_user_by_email(email):
    """get user by email"""

    return User.query.filter(User.email == email).first()



#<<< ------ Client queries ------ >>>#

def get_all_clients():
    """return a list of all clients"""
    
    return Client.query.all()


def get_client_by_client_id(client_id):
    """get client by client id"""

    return Client.query.filter(Client.client_id == client_id).first()


def get_client_by_lname(lname):
    """get all clients by this last name"""

    return Client.query.filter(Client.lname == lname).all()



def get_client_by_fname(fname):
    """get all clients by this last name"""

    return Client.query.filter(Client.fname == fname).all()


def get_client_by_fname_and_lname(fname, lname):
    """get all clients by this last name"""

    return Client.query.filter(Client.fname == fname & Client.lname == lname).all()


def get_client_by_email(email):
    """get client by email"""

    return Client.query.filter(Client.email == email).first()


#<<< ------ Appointment_rec queries ------ >>>#

def get_all_appointment_recs():
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


#<<< ------ Appt_img queries ------ >>>#

# def get_all_appt_img():
#     """return all appt_imgs"""

#     return Appt_img.query.all()


# def get_appt_img_by_id():
#     """return all appt_imgs"""

#     return Appt_img.query.filter(Appt_img.img_id).all()


# def get_appt_img_by_appt_rec(appt_rec_id):
#     """return imgs from appt_rec_id"""

#     return Appt_img.query.filter(Appt_img.appt_rec_id == appt_rec_id).first()


# def get_appt_img_by_date(img_date):
#     """return a list of images from this date"""

#     return Appt_img.query.filter(Appt_img.img_date == img_date).all()


# def get_appt_img_by_client_id(client_id):
#     """return a list of appt_imgs for client_id"""

#     return Appt_img.query.filter(Appt_img.client_id == client_id)


# def get_appt_img_by_user_id(user_id):
#     """return a list of all appt_img for user_id"""

#     return Appt_img.query.filter(Appt_img.user_id == user_id)


#<<< ------ Product queries ------ >>>#

def get_all_products():
    """return all products"""

    return Product.query.all()

def get_product_by_id(product_id):
    """return product by id"""

    return Product.query.filter(Product.product_id == product_id).first()


def get_product_by_name(product_name):
    """return product by name"""

    return Product.query.filter(Product.product_name == product_name).first()


def get_all_product_names():
    """return a list of all product names"""

    return Product.query.filter(Product.product_name).all()
    

def get_product_by_product_categories(product_categories):
    """return a list of all products in the category"""

    return Product.query(Product.product_categories == product_categories).all()

#<<< ------ Service queries ------ >>>#

def get_all_services():
    """return a list of all services"""
    
    return Service.query.all()


def get_services_by_id(service_id):
    """return a service by id"""
    
    return Service.query.filter(Service.service_id == service_id).first()


def get_services_by_name(service_name):
    """return all service names"""
    
    return Service.query.filter(Service.service_name == service_name).first()






    




    

if __name__ == '__main__':
    from server import app

    connect_to_db(app)
