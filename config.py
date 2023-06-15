# Flask is going to look for things with SPECIFIC names so it is important that you give the files a certain name not random names. That is why the instructor named the files and folders this way. for example:  app, __init__.py, config. ALL of the files OUTSIDE of the app folder are meant to work around our app to help configure it. Thats what the 'config.py' file is for. It helps our computer and app communicate with each other.

#When we add the app to the internet config allows our application to talk to the internet 

# Part of the configuration process is getting our app to a place where it can talk to whatever its running on, because eventually were going to have this run on the cloud, and other peoples devices. The first thing we do is import os

import os # This is a module that allows us to talk to the operating system, because we are taling to the compute
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__)) # Here is a line of code we use to connect the dotes to other paths because our application is talking to the computer back and forth. WE NEED this code but not going to explain its purpose. You can google it
load_dotenv(os.path.join(basedir, '.env')) # were allowing our configuration file to talk to our computer when we call on this file to operate

class Config(): # Our class config
    """
    Set config varibles for the flask app 
    using Environment variables where available.
    Otherwise, create the config variable if not done already.
    """

    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Sharmain' # This is for security purposes this line of code can also be written like this(SEE BELOW)
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'Ryan will never get access to my CSS' You can type whatever you want in the string
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db') # We added or 'sqlite:///' to allow us to use other SQL languages for our databases just in case it doesnt work right. 
    #Here we are using SQLALCHEMY to interact with our database later on 
    SQLALCHEMY_TRACK_MOIFICATIONS = False