# Flask is going to look for things with SPECIFIC names so it is important that you give the files a certain name not random names. That is why the instructor named the files and folders this way. for example:  app, __init__.py, config. ALL of the files OUTSIDE of the app folder are meant to work around our app to help configure it. Thats what the 'config.py' file is for. It helps our computer and app communicate with each other

#Models.py will help us with our databases so we dont have to write SQL tables and SQL queries, we will automate alot of that stuff

from flask_sqlalchemy import SQLAlchemy # SQLAlchemy is the main import we will be using to handle our data to pass back and forth our data to our database
from flask_migrate import Migrate #Migrate is responsible for uploading our data tables. These are ALL imports that write SQL for us so we dont have to 
import uuid # uuid - universal unique identifier, which will be a distinct string of numbers that were going to use for primary keys for things. It will keep things unique, even if multiple people log on with the same name but are different people. Their data will be kept seperate
from datetime import datetime # When we call on this module it will give us the date and time
from werkzeug.security import generate_password_hash, check_password_hash # #werkzeug(verk-zoyg) means tool in German. werkzeug security are packages that are meant to encrypt our passwords so that users can create login information/password information. However If  someone were to access that database you would be able to see the name and email probably but not the raw data like passwords because it will become a string of numbers rather than what was typed into the website.
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow # This also helps with moving data back and forth, particularly if you have collection of data
import secrets

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy() # db will be a database for SQLalchemy

@login_manager.user_loader 
# Here is our decorator for login manager, this is basically like writing a route, when this code is executed eventually when we run the program this code will help find the user that is being looked for and load it, and be held in memory. This is the part where we create names for the tables information
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin): #This apart of making our database, below are variables that include column data, when we instantiate the class and migrate the data to our database, it will end up creating the tables automatically for us 
    id = db.Column(db.String, primary_key=True) # Primary key is useful and should be true to make sure the id is the primary key, not  their name because two different people with the same name might try to create accounts. There would be a problem if their name was their primary key, so we use an 'id' thats going to be universally unique identification
    first_name = db.Column(db.String(150), nullable=True, default='') # the string is limited to 150 characters
    last_name = db.Column(db.String(150), nullable = True, default = '') #nullable is the same thing as typing NOT NULL
    email = db.Column(db.String(150), nullable = True) # You do need to have an email and must enter an email so nullable = True. NOT NULL/Nullable enforces a column to not accept NULL values
    password = db.Column(db.String, nullable = True, default = '')# Were allowed to have empty values for certain things but  we still have to create the columns so 'default = 'nothing'
    g_auth_verify = db.Column(db.Boolean, default = False) # default is not an empty value here anymore
    token = db.Column(db.String, default = '', unique = True ) #Here we want to make sure our token is unique for each user/ sort of like tracking who is using our website and make sure their actually allowed. The token is something that is generated when someone makes an account. SO later on when someone tries accessing our phonebook, you want to make sure they ACTUALLY created an account with us and isnt random, so, someone that is part of our system 
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) # when the user is created the date_created will be made so we know when the user started their account
   
    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

# below are tokens for self_id set_token etc.
    def set_token(self, length):
        return secrets.token_hex(length) # Here were sending back a token hex and the length will be 24 characters long

    def set_id(self): #when we run user id it will generate an id for our user, a bunch of unique numbers and letters
        return str(uuid.uuid4())
    
    def set_password(self, password): #  When the user makes their password its going to run the set.password and take the information from above and pass it down here, its passing data back and forth
        self.pw_hash = generate_password_hash(password) # This line will generate a password hash only werkzeug has the ability to undo that. BUT they cant see our databasewhich ends up being mutual security set up
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database' #This is confirmation that what just happened happened
    # This whole class is for users to create accounts and login, we need our database to hold that information, whos made accounts, what data is associated with that account so that the user can login/logout, sign up etc.


# We also need another class (the class below) for our database of our actal contacts, of the actual things we end up storing. So when our users need to add a new contact to their phonebook, the contact has a database already ready to go, where we can store their name, phone number, email etc. AND they need unique ids and a user token
class Contact(db.Model):
    id = db.Column(db.String, primary_key = True) #id takes care of its ownself as far as the amount of characters
    name = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(200))
    phone_number = db.Column(db.String(20)) #20 characters in case someone wants to add dashes, or international code plus their phone number 
    address = db.Column(db.String(200))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,name,email,phone_number,address,user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.user_token = user_token # We dont have to write a function for set_token etc. below because were pulling from somewhere else (see above class)


    def __repr__(self):
        return f'The following contact has been added to the phonebook: {self.name}'

    def set_id(self):
        return (secrets.token_urlsafe())

class ContactSchema(ma.Schema): #This is where marshmallow comes in 'ma' which has to do with connecting the dots
    class Meta:
        fields = ['id', 'name','email','phone_number', 'address']

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)
