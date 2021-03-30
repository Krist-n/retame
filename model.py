from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from faker import Faker

# fake = Faker()
app = Flask(__name__)

db = SQLAlchemy()

class User(db.Model):
    """A user (stylist, colorist, barber)."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_name = db.Column(db.String(15), unique=True)
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
    return f'<Client client_id={self.user_id} email={self.email}>'

class Appointment_rec(db.Model):
    """Appointment Records."""

    __tablename__ = 'appointment_recs'

    appt_rec_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    appt_date = db.Column(db.DateTime, nullable=False)
    service_notes = db.Column(db.String, nullable=False)
    tools_used = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('appointment_recs.user_id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'))
    service = db.Column(db.String, db.ForeignKey('services.service_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))

    user = db.relationship('User')
    client = db.relationship('Client')
    service = db.relationship('Service')
    product = db.relationship('Product')

    def __repr__(self):
        """Show appointment records info"""
        return f'<Appointment_rec appt_rec_id={self.appt_rec_id} user_id={self.user_id} client_id={self.client_id}>'

class Appt_img(db.model):
    """Image taken of service"""

    __tablename__ = 'appt_imgs'

    img_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    url = db.Column(db.String, nullable=False)
    appt_rec_id = db.Column(db.Integer, db.ForeignKey('appointment_recs.appt_rec_id'), nullable=False)

    def __repr__(self):
    """Show image info"""
    return f'<Appt_img img_id={self.img_id} appt_rec_id={self.appt_rec_id}>'   

class Product_category(db.Model):
    """Category a product is used in"""

    __tablename__ = 'product_categories'

    product_category_id = db.Column(db.Integer, 
                                autoincrement=True,
                                primary_key=True)
    category = db.Column(db.String, nullable=False)

    product = db.relationship('Product') 

    def __repr__(self):
        """Show product category"""
        return f'<Product_category product_category_id={self.product_category_id} category={self.category}>'   

class Product(db.Model):
    """A product."""

    __tablename__ = 'products'

    product_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String, db.ForeignKey('product_categories.category'), nullable=True)
    
    category = db.relationship('Product_category')

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
    price = db.Column(db.Integer, nullable=False)

    appt_service = db.relationship('Appointment_rec')
    service_tools = db.relationship('Service_and_tool')

    def __repr__(self):
        return f'<Service service_id={self.service_id} service_name={self.service_name}>'

class Service_and_tool(db.Model):
    """Association table"""

    __tablename__ = 'services_and_tools'

    service_and_tool_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'))
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.tool_id'))
    
    tool = db.relationship('Tool')
    service = db.relationship('Service')

class Tool(db.Model):
    """Tools used by the user"""

    tool_id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    tool_name = db.Column(db.String, nullable=False)
    service_specific_tool = db.Column(db.String, nullable=True)


# def connect_to_db(flask_app, db_uri='postgresql:///ratings', echo=True):
#     flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
#     flask_app.config['SQLALCHEMY_ECHO'] = echo
#     flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     db.app = flask_app
#     db.init_app(flask_app)

    # print('Connected to the db!')



    





if __name__ == "__main__":
    from server import app