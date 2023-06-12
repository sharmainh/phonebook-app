# We ALREADY imported flask in the __init__.py file FIRST. Instead we want to pull in blueprint

from flask import Blueprint, render_template

site = Blueprint('site', __name__, template_folder = 'site_templates') # Here we created a variable, site to instantiate the blueprint class. __name__ is tying this content to our __init__.py file. site_templates comes frrom the folder we created. This means that the routes were going to take will know to look for the templates IN HERE

#WHY USE THE NAME SITE as a variable, it is relevant to what is happening, therefore were seperating concerns. ALl of the stuff thats related to how the SITE is rendering will be kept in a site folder

@site.route('/') # Createing a decorator here
def home(): #This is where we create the home page, When the code runs THIS will be the home page/fiirst paget that shows up with the base html extended around it
    return render_template('index.html') # This wont work just yet up to this point. Theres still more code to write

@site.route('/profile')
def profile():
    return render_template('profile.html')


