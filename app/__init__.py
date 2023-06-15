# The api folder will have all of the rules for how the outside entities, like other back end applications or front end applications would be able to talk to our app and say "hey I would like this data". We will tell them what they have to request to get the data, how they can add data, how they can delete data

#authentication is going to be all of our rules for creating users, logging them in and logging them out, because people are going to be able to sign in and make accounts. Then theyll have access to the data

#Site folder is going to be the rules for our webpages. SO our homepage

#Static folder is very important that we name it static because flask is going to look for images inside the static folder. CSS and images will live in this folder because they dont change their just going to stay the same way 

#Templates, we will use alot of HTML templates to automate our work. SO we dont have to do as much work everytime we want to make a new page. It will keep the website consistent and running smooth

#The __init__.py file is where we are going to run most of our logic. The file where we actually end up running the app. Where we instantiate all of our classes and get all of the parts moving all at once

# We are doing something called seperation of concerns. Instead of writing ALL of the code in one file it would be difficult to debug so we seperate code in different files. Each file has a different role and task 

from flask import Flask

from config import Config # Here were saying from the config file import the class Config in config.py. This is how we import the class
from.site.routes import site # site.route is a path you need to follow to get to site site is the folder name (.) is seperator and routes is the name of the file where the variable site is located. Now we dont need to navigate to the folder
from.authentication.routes import auth 
# What this is doing is going to routes.py and pulling all of the blueprint from line 8 auth = Blueprint('auth', __name__, template_folder='auth_templates') which includes all of the decorators that goes into it, and the template folder that comes with it. It ends up running it inside of the __name__ which is what our app is running inside of app = Flask(__name__) - This is the line of code that runs our app (see below)
from.api.routes import api # Were pulling in our api here
from flask_sqlalchemy import SQLAlchemy #The orange squiggly line is because there arent any folders that hold these modules yet, they havent been installed into our application
from flask_migrate import Migrate
from models import db as root_db, login_manager, ma
from flask_cors import CORS # CORS is for security purposes, this part is where we import the module (This doesnt mean youve installed it yet) CORS will help prevent cross site request forgery. It can be annoying if you dont set it up correctly. It wont let you use the app and think your stealing data if not set up correctly. By adding CORS it keeps our application more secure
from helpers import JSONEncoder #Here were importing JSONEncoder from helpers.py


app = Flask(__name__)
CORS(app) # This line of code should go right after the above line of code. By putting CORS in the app like this we will have to make sure that any other applications we connect to it have the right permissions

app.register_blueprint(site) # This is where were building the site folder, and how we register the blueprint for site
app.register_blueprint(auth) #This is where we register the blueprints for our off sites. The orange squiggly line means you need to import the module (see above)
app.register_blueprint(api) # Where we register the blueprints for the api folder

app.json_encoder = JSONEncoder 
app.config.from_object(Config) # This line of code allows the configuration to work, the database will connect and the .env file should also be connected
root_db.init_app(app) # initiating the app and making the database
login_manager.init_app(app) # We are applying this to the application that is being made
ma.init_app(app) # We are applying this to the application that is being made
migrate = Migrate(app, root_db) # We are applying this to the application that is being made. Were Creating a migrate class here were instantiang the migrate class for the app and root db. This code might not run up to this point if the api routes havent been created  once we create the api folder and import these



# Working our our virtual environment: What does that mean? Well at the very top of our code there are a few things that were trying to import but they are not installed. Typically you would think to just download/install it Yes and No. Imagine your working on a project for a company and the company wants you to use some OLD python files from like 5-10 years ago (pythons been around for about 15 years) and the files are in python 2, however your computer might have python 3 installed and in order to run python 2 you would have to uninstall python 3 and install python 2 which can be challenging and then update the documents/work on them. HOWEVER you might NOT WANT to reinstall and uninstall things etc. it can be a huge pain. SO what we do to solve that is CREATE VIRTUAL ENVIRONMENTS, additionally, when we put our applications on the cloud, usually the servers on the clouds run Linux, If your running WINDOWS thos two things dont get along well (Mac and Linux) get along a LITTLE better.(the linux servers are basically blank slates, they dont come with anaconda, or python installed etc) Therefore you need to be able to tell linux severs "hey install python for my application", There are pros and cons, this way you wont have to reinstall and uninstall things on your device you can just put them on linux and work out of there. Were not going to work on the cloud for our application , but we will create our own world, so for our application were installing things JUST into our app, and then were going to put it on the internet, were going to tell the linux servers please install these things to the area that youve allocated for our application so that our applucation will run. And then when users ping our application/try to use it our application will run just fine because it has all the pieces that it needs to install and nothing else because thats the whole deal with storage, your buying storage so you dont want to add extra stuff in there because you have to pay for that (so were going to install ONLY the things we actually need for our app to run ). Some things happen automatically where we dont have to write "please install python". The  servers are able to realize what it is were putting on here as your building. The servers will detect a python app for example. BUT some things like SQLAlchemy it wont pick up automatically. SO we need to install these things on our own, which is fine and and thats why we use a virtual environment. 
#WERE GOING TO CREATE a little world for our app to use and install things into, like a folder we install things into inside of our project, It will then be able to use the things that it installed into that folder to run its code. We will need to create a virtual environment we will be writing it for Mac.

#CREATEING VIRTUAL ENVIRONMENT STEPS! you can always use quit() command in terminal if need to start over quit()
# Step One: type 'python3 -m venv venv' in a cleared/new terminal (this should be the same on windows) press ENTER
#(This means were going to call our virtual environment)venv is short for virtual environment. Then you will see a venv folder appear, with other folders, and files etc. When you call pip, things happen automatically that you dont have  to understand, BUT theres alot of magical stuff inside of our Library and venv, which is helping us communicate with the servers when we put it on there and very directly say install these things

# Step Two: (This is the windows version you type in the terminal) 'venv\Scripts\activate' Press ENTER You can use a different folder name than venv if you want IF you do change the lines of code that have venv to the name of the folder you want to use (This is the Mac version) 'source venv/bin/activate' ENTER - What this is doing is turning the venv on it is actually saying "I want to operate my app inside of this virtual environment" you will ALSO se venv in the terminal. This looks very simialar to the conda environment because they do very similar things

# Step Three: Type 'conda activate' ENTER then in the terminal you will see you have both venv and base operating AND NOW we will be able to start installing things.

# Step Four: 'pip install alembic' ENTER - If you type this command and it already exists thats fine

#Step Five: 'pip install click'
#Step Six: 'pip install dnspython'
# Step Seven: 'pip install Flask'
#Step Eight: 'pip install email-validator'
# Step 9: 'pip install flask-cors' All of these things were installing are on the notion document
# You can see what youve already installed in your virtual environment in the terminal by using 'pip freeze' for this project you do not need all of the pip installs. You just need the ones from this document https://yummy-seeder-cf8.notion.site/Virtual-Environment-ef5389de15884ae0aa999d1f9dd7c7fe

#'pip freeze > requirements.txt' This will load a documen(txt file) on the right in the explorer area and you can see all of the things installed. Alot of the things you see in the txt file are already installed on your computer. Instead of all of the installs you can DELETE them and paste whats needed for example https://yummy-seeder-cf8.notion.site/Virtual-Environment-ef5389de15884ae0aa999d1f9dd7c7fe copy and paste the list of things to install via Pip.
#The requirements.txt document is what interacts with the venv folder. When we end up hosting this Heroku/The cloud platform were using looks for requirements.txt document to figure out what to install, then the app will run just fine.

#Migrations process/Transfer Data to DATABASE STEPS AFTER SETTING UP THE ABOVE STEPS (You should have migrations folder, VENV FOLDER, and .ENV UP TO THIS POINT)

# STEP 1 in the terminal type 'flask db init' return (were initializing the database here, you will also a new migrations folder) (if theres an ERROR: Attribute Eror json Encoder- from json import JSONEncoder, if db cannot be found exit all terminals in VSC CTRL-C, shut down/refresh application then try again)

#STEP 2 in the terminal type 'flask db migrate' return (this will start moving things and getting things ready to share, alembic comes into play)

#STEP 3 in the terminal type 'flask db upgrade' (this will put stuff in the database)

#STEP 4 'flask run' to view webpage/run application

#After running application to test for bugs, head to database/elephantsql in this case and check 'table queries', 'user' table to make sure a token was created and proof that password is encrypted


















