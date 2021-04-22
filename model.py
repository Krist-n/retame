from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    """A user (stylist, colorist, barber)."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String(15), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    user_appt = db.relationship('Appointment_rec')

    def __repr__(self):
        """Show info about user"""
        return f'<User user_id={self.user_id} email={self.email}>'
    


class Client(db.Model):
    """A client"""

    __tablename__ = 'clients'

    client_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    
    client_appt = db.relationship('Appointment_rec')

    def __repr__(self):
        """Show info about client"""
        return f'<Client client_id={self.client_id} email={self.email}>'


class Appointment_rec(db.Model):
    """Appointment Records."""

    __tablename__ = 'appointment_recs'

    appt_rec_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    appt_date = db.Column(db.DateTime, nullable=False)
# Client notes per section and perosnal
    tools_used = db.Column(db.String, nullable=False)
    back_panels = db.Column(db.String, nullable=False)
    right_panel = db.Column(db.String, nullable=False)
    left_panel = db.Column(db.String, nullable=False)
    top_panel = db.Column(db.String, nullable=False)
    front_panel = db.Column(db.String, nullable=False)
    personal_notes = db.Column(db.String, nullable=False)
    img_path = db.Column(db.String, nullable=True)


    user_id = db.Column(db.Integer, 
                    db.ForeignKey('users.user_id'),
                    nullable=False)
    client_id = db.Column(db.Integer, 
                    db.ForeignKey('clients.client_id'),
                    nullable=False)
    service_id = db.Column(db.Integer, 
                    db.ForeignKey('services.service_id'),
                    nullable=False)
    product_id = db.Column(db.Integer, 
                    db.ForeignKey('products.product_id'),
                    nullable=True)
    img_id = db.Column(db.Integer, 
                    db.ForeignKey('appt_imgs.img_id'),
                    nullable=True)


    def __repr__(self):
        """Show appointment records info"""
        return f'<Appointment_rec appt_rec_id={self.appt_rec_id} user_id={self.user_id} client_id={self.client_id} \
            appt_date={self.appt_date}>'


class Appt_img(db.Model):
    """Image taken of service"""

    __tablename__ = 'appt_imgs'

    img_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    img_path = db.Column(db.String, nullable=False)
    img_date = db.Column(db.DateTime, nullable=True)
   
    appt_img = db.relationship('Appointment_rec')

    def __repr__(self):
        """Show image info"""
        return f'<Appt_img img_id={self.img_id} img_url={self.img_path}>'   


class Product(db.Model):
    """A product."""

    __tablename__ = 'products'

    product_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product_category = db.Column(db.String, nullable=True)
    

    def __repr__(self):
        return f'<Product product_id={self.product_id} product_name={self.product_name}>'


class Service(db.Model):
    """Services performed"""

    __tablename__ = 'services'

    service_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    service_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    appt_service = db.relationship('Appointment_rec')

    def __repr__(self):
        return f'<Service service_id={self.service_id} service_name={self.service_name}>'




def connect_to_db(flask_app, db_uri='postgresql:///retame', echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')



if __name__ == "__main__":
    from server import app


    connect_to_db(app)