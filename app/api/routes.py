from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Contact, contact_schema, contacts_schema

api = Blueprint('api',__name__, url_prefix='/api') #This is the same line that we use in our other routes. Similar to the auth in the other routes.py file and site routes in the other routes.py file one of the attributes sets template folder = templates telling the computer wher ethe template folder is for our site route. However we dont have one of those here. However you can add more attributes to this particular object other than 'api',__name__, url_prefix='/api'. same thing applies to the other routes attribues. Were seperating our interests and keep things apart from one another, some of the attributes are not needed here. Were keeping all of the api's categorized, keeping them in one folder. This line of code means that everytime we write our api route we have to write out '/api' before the slug/very last part of our URL

#Here we write some api routes to put data into our database 

@api.route('/getdata') # When we go to the link/slug 'getdata' it will render yee haw on the webpage is all these lines of code does. If you test the code 'flask run' YOU MUST use the url prefix 'api' in the url plus slug for example http://127.0.0.1:5000/api/getdata. When you visit the webpage it returns some json
def getdata(): #takes no parameters
    return{'yee':  'haw'} #This looks like a dictionary but thats not what were calling it.

@api.route('/contacts', methods = ['POST']) 
@token_required
def create_contact(current_user_token):
    name = request.json['name'] #This line of code will look at json and bring back the name, but the key of that name, name on one side and the value on the other (key, value pairs) name is the key. name will be before the equal and value after the equal
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']
    user_token = current_user_token.token
#POST means were allowed to send data to the api, it sends information to the database
 #token-required will execute the the entire code from helpers.py to make sure NOTHING will happen until we have our token. It will keep looping the code over and over and over again until it gets what it wants.
 #cureent_user_token is created in helper.py when the token required function is executed

    print(f'BIG TESTER: {current_user_token.token}') #current_user_token that came from token required (see above notes) were printing the token number

    contact = Contact(name,email, phone_number, address, user_token = user_token) # Here were using the entire Contact class that was in models.py the parameters match what is in models.py except token and id were not writing it, the code will do it for us. user_token will overwrite the default value the class had and save everything to the variable contact. NOW that everything is saved to our variable we will add this to our database below

    db.session.add(contact) #You still have to commit it after this step
    db.session.commit()

    response = contact_schema.dump(contact) 
    return jsonify(response)
     #This contactschema is from models.py also, which will end instantiating a class and dump the current state of the schema to a database. When we run this function whatever we end up sending to it will show us on our api in insomnia

@api.route('/contacts', methods = ['GET']) #Earlier in the above code we used POST this time we will use GET
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    contacts = Contact.query.filter_by(user_token = a_user).all() 
    response = contacts_schema.dump(contacts)
    return jsonify(response)
    #a_user is the actual token number, the all function is bringing back all of the users we have in our database
    

#Insomnia api rest is a website that allows us to make and take api calls, you can use this platform to test your routes to make sure the data that we want to come through is coming through. This way we dont have to design an entire website on the front end to practice taking api calls. You can write JSON design api's on this website etc.

# When you load the insomnia application click create, then request collection, type the name of your project. Then 'command N' to create a new request, use GET (GET request) and type the name 'Get Data' (it can be something different). Next to the send button copy paste the api url above http://127.0.0.1:5000/api/getdata (this is one of many other urls). Then press send and you will see it brings us back our data which proves the data that we meant to retrieve is coming back correctly. The green 200 means the request succeeded

#What if you want a specific contact, we can call it with an ID number. This is OPTIONAL
@api.route('/contacts/<id>', methods = ['GET']) #When you put something inside of the URL/ inside of braces thats a variable. The id is something we will be able to call back and put into the rest of our function. This will be a get method.
@token_required #We rquire a token
def get_single_contact(current_user_token, id): # the slud 'id' becomess a variable above can be passed into this function
    contact = Contact.query.get(id)
    response = contact_schema.dump(contact)
    return jsonify(response)

# UPDATE ENDPOINT update one of the data points (see below)
@api.route('/contacts/<id>', methods = ['POST', 'PUT']) # if our CHANGING something in your data you have to retrieve(POST) that information then put it back(PUT)
@token_required
def update_contact(current_user_token, id):
    contact = Contact.query.get(id)
    contact.name = request.json['name']
    contact.email = request.json['email']
    contact.phone_number = request.json['phone_number']
    contact.address = request.json['address']
    contact.user_token = current_user_token.token
    
    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

#To test the above code, a new request was created in insomnia called update contact, You can type in the console the key, value pairs you would like to change You should be able to copy the id from one of the users and paste it with url at the top where the url typically goes http://127.0.0.1:5000/api/contacts/KXOgP16YurjO5ILqReRPdOEuBWPdjuLX_tH_Pqclsx4.
# DONT FORGET TO GO TO HEADER TAB add the x-access-token (left side)  (right side)paste token from profile page or sql database

# DELETE USERS/Delete Endpoint from the Database
@api.route('/contacts/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    contact = Contact.query.get(id) # its going to pull back contact data from our database based on what the id is
    db.session.delete(contact)
    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

# quit and run flask again, create a new delete request in insomnia (see phonebook application) , Enter Headers information including token id, url etc. send then it will show you who was deleted. go to get contacts to see deleted user

# AFTER COMPLETING EVERYTHING AND ITS TIME TO SUBMIT THE PROJECT 1st: deactivate conda otherwise it will cause problems. also in requirements.txt python - dotenv version ==o0.19.0 does not work with render DELETE THE VERSION NO MATTER WHAT IT IS THE VERSION THAT IS COMPATIBLE WILL BE ADDED AUTOMATICALLY. Once thats done, update github type 'git add .' in terminal, 'git commit -m "updating my req for render"', git push - u origin main


