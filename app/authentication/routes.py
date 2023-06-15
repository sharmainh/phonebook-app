# When we want to declare our routes for our app to run we will call on routes.py
from forms import UserLoginForm #This will route to forms.py, besides you cant just import an html file so its NOT forms.html. This is Python, this is a module which is why were using extends AND routes.py is a Python file
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user, LoginManager, current_user, login_required # All of these words will turn blue when everything is created

auth = Blueprint('auth', __name__, template_folder='auth_templates') # Here for the auth routes we have labeled where the templates are

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()

    try: # We need a try catch here just in case the user tries to give us the wrong information for an email for example say its a phone number instead of an email. This will tell users what they did wrong
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data # The user enters their email on the forms.html first then this will go to the UserLoginForm (see above) it will take the email, specifically the data from the email section of our user login form (see forms.py), check the parameters in forms.py to see if what the user entered counts as an email. If it does we will save it to THIS email variable above. SAME THING APPLIES TO password below
            password = form.password.data
            print(email, password) # when testing the code DONT use personal information as long as you use email format the code will work. This line of code is ONLY USED WHEN YOUR TESTING THE APPLICATION BECAUSE IT ACTUALLY PRINTS THE USERS EMAIL AND PASSWORD. DELETE THIS LINE WHEN FINISHED WITH THE APPLICATION

            user = User(email, password = password) # inside the user class we will take the password above and set it equal to this password, were passing data from place to place. Then this email gets saved into the database in models.py

            db.session.add(user) #db comes from SQLAlchemy in models.py, which is part of adding information to the database. #This line of code takes all of the information in (user) from models.py and make it ready to go
            db.session.commit() # this line is very similar to a git hub push 



            flash(f'You have successfully created a user account {email}', 'User-created') #This flash function is like a pop up that lets users know that it worked. You will have to write some java script to handle this or python. BUT it is ready for you to write some python flash pop up code if you would like. (THIS IS AN EXTRA CREDIT ASSIGNMENT) # 'User-created' is used to talk to our application
            return redirect(url_for('site.home')) # This line will llook for the route in routes.py, site.home will look for the function home. The 'url_for' Just means its going to generate the url for that page to execute. So after the user creates their account it will send them back to their home page.
        
        #What if what the user inputs doesnt work!? in our Try, then we catch/except no if else statement is required (see below)
    except:
        raise Exception('Invalid Form Data: Please Check your Form') # As long as users on this webpage its going to keep sending a message if the information is incorrect
    return render_template('sign_up.html', form=form) #Even though theres a problem, when we call the sign up page it will still render template for sign_up.html

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm() # Need parenthesis to instantiate the class
    try: # For signing in we need our try catch again
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            logged_user = User.query.filter(User.email == email).first() # The purpose of this line is to take the email data, check it against the user class,then query our database, filter through all the data that meets that parameter/requirement and pull back the first one that comes back from that email. The email should be unique so it should pull back one account, and that will be our 'logged_user' that were going to hold on to.
            if logged_user and check_password_hash(logged_user.password, password): # check_password have is imported from models.py (see modules above). logged_user.password will pull back the hash value from our database, because we encrypted the password name by werkzeug. It will give us the hash password. check_password_hash will unhash that password and then check it against 'password' (password variable after logged_user.password). It will take the password values dehash it and see if the password passed is accurate. 'logged_user' in this line of code is saying whether or not the email was in the database
                login_user(logged_user) # If the credentials match/ The if statement above is truthy then we will login the user
                flash('You were successful in your initiation. Congratulations, and welcome to the Jedi Knights', 'auth-success') # 'auth-success' is used to talk to our application
                return redirect(url_for('site.profile')) # Once their signed in it should send them to their profile page
            else: # However if the email or password or both are inaccurate Then below we send the user a message
                flash('You do not have access to this content.', 'auth-failed') # auth-failed will talk to our application and say hey their login did not match, login failed
                return redirect(url_for('auth.signin'))
    except: # Here is except used to handle an error
        raise Exception('Invalid Form Data: Please Check your Form') # If their not giving us a valid email or the right password It will show this line of code to let the user know they didnt bring in the right information. 
    return render_template('sign_in.html', form=form)

@auth.route('/logout') # This route is for logging the user out, because we want users to be able to logout
def logout():
    logout_user()
    return redirect(url_for('site.home')) # This will return the user back to the homepage