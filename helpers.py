# The helper file helps make sure users can login correctly and makes sure users have the right to access our api data. For example: if you create a phonebook with different peoples contact information, you only want certain people to be able to see that 
#The helpers file is going to create extra function to check tokens for rightful access to our content. So when we make our api(our api is the part of our application that handles the data that we want to see. The api is going to be all the rules for our contacts in our phonebook. For example, if your on instagram, you have your authentication, you got your site, you can still be logged into your application, and you can still have access to the way the app looks, but if you have the internet turned off on your phone and you try to open facebook or instagram stuff will still display but there wont be any content. The api is the part where were actually interacting with our content and the data that comes back). For the helpers function were going to use these tokens and thats going to ensure that whoevers looking at our data actually has the right to do it. if they DONT have the right token or the right access to the data, it will deny them permission to see the content
from functools import wraps # functools comes from python 
import secrets # similarly to our models page
from flask import request, jsonify, json # json is a part of javascript. json is content that javascript is able to parse really easily. Its very similar to the way that python works through stuff. SO we will be able to use python to traverse that data as well AND JSON is a very common/popular way for data to be delivered that way as developers were able to work through it.
from json import JSONEncoder
import decimal

from models import User

#were going to write a function in here thats going to require that our users are doing what their suppossed to. 
def token_required(our_flask_function): #This is some magic backend stuff. You can use this exact same function anytime you require a token 
    @wraps(our_flask_function)
    def decorated(*args, **kwargs): # (*args, **kwargs)  means for however many tokens we end up adding to this we want thos function to be able to carry that data. This is another function but its inside of 'token_required' function whats going on here is weve got the flask function running. and were going to return decorated at the end of this function which means the function will keep running for however long we keep calling the function
        token = None

        if 'x-access-token' in request.headers: #This entire process below will check whether the token is valid and make sure users are doing what their suppossed to 
            token = request.headers['x-access-token'].split(' ')[1]
            #Eventually we will have a bearer token and its going to take a token number thats passed in and check if its a valid token. Above we have a key, value (headers['x-access-token']) set up headers is the dictionary access-token is a key. When we call headers['x-access-token'] its going to return the value which is the bearer token part 
        if not token:
            return jsonify({'message': 'Token is missing'}), 401 # This is going to make a json item that we can pass back to the person trying to view our data by sending a message to tell the user theres something wrong. Then we will throw back a 401 error(404's are more common but 401's happen as well). Were trying to give our code directions on how to tell us theres something wrong and what is wrong. WHich will be useful when your debugging your code. 
        try:
            current_user_token = User.query.filter_by(token = token).first()  #This is a new variable. We go to the user class (weve imported user already above) were going to ask it for something were going to filter it by token and Its going to be the first thing that comes up based on what our token ends up being written out as. Again, were taking the token from the request.headers etc(see above). So when the user wants to look at some data and has a token, we save their token to the token variable above. That value will go here in this line of code 'token = token' Then the cpu will search in User(in our database) for a user that has that token, whatever the one that comes back is what were going to end up saving to our current users token. All were doing is carrying data from place to place. Again, from requests(The user enters their login information/token) were saving that data, checking it in the database if it is were going to assign that to 'current_user_token'  
            print(token) #Then we print the token for our app to look at, it will be in our terminal
            print(current_user_token) # Whern the token reuired function above runs, end will end up bringing that data, elsewhere and we can use it in other places

        except:
            owner=User.query.filter_by(token=token).first() #Were doing the SAME thing here, pulling the token back and setting it as owner. So if the current token doesnt work/come back correctly then we know that theres an issue. The if statement checks If the user did/didnt even give a token. the try is checking to see if the token is in the database

            if token != owner.token and secrets.compare_digest(token, owner.token): # secrets.compare_digest is from the secrets import this function uses an approach designed to prevent timing analysis, making it appropriate for cryptology(use mouse pointer to hover over the words compare_digest and secrets to see an explanation/details). This is a security setting thats all that secrets is. SO were going to compare the two, take the token, see if it matches the 'owner token'. But this is the secret hidden version because were trying to prevent someone from looking at what the original data was 
                return jsonify({'message': 'Token is invalid'}) # If the tokens are not matching theres our message
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated #  Every time were running this entire code, we want to keep calling the function and checking if the token is valid or not. We want to prevent it from letting the user in if the token doesnt work, we want to keep holding the user back until the token works

class JSONEncoder(json.JSONEncoder): 
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): #This is checking to see if the object is a certain datatype
            return str(obj) #and if it is the coreect data type were going to make a string version of it so that we can use it in other places
        return super(JSONEncoder,self).default(obj) # if its not the correct data type we return the object itself

# To test contact code you can use insomnia, Create a new request within the application folder. Set the method to 'POST', and the text to JSON. Create a dictionary with sample contact information in the console that includes the names of the keys in the code for example (see above)
#  {
	# "address": "1 Main Street Alaska",
# 	"email": "applesandoranges@can.com",
# 	"name": "Sharmain",
# 	"phone_number": "555-555-5555" 
# }
#Then to test the code in insomnia 'flask run' to retrieve the url http://127.0.0.1:5000/api/contacts must include api, and contacts is from @api.route('/contacts) see above. Click send  if it returns "token required" thats good, it shows the program is working properly. helpers.pyy has token required information.

#You can check the headers tab in insomnia to make sure it says content-type(left)  (right)application/json if not you can add that yourself. The add a new header x-access-token(left side) (right side) Bearer (token id) You can retrieve token id from database or sign in to user account (see insomnia phonebook app for example)
# See line 17 to understand x-access-token. request.headers[x-access-token] is the same as request.json except instead of looking at JSON in insomnia were looking at header tab. The key is x-access-token which will bring back Bearer (token id) (see insomnia for bearer etc.) looking at line 17, it will split bearer and only take the access token and save it to 'token' variable. Click send and you will see an id will be created in the dictionary automatically because when models gets instantiated/class Contact is called self.id will run and create a secret id number that is unique. This means we sent data and can now go to the database click 'table inqueries', 'contact' 'execute' The user token will be who created the account because it matches with the profile id

