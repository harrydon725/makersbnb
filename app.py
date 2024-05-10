import os
from flask import Flask, request, render_template, redirect
from lib.database_connection import get_flask_database_connection

from datetime import datetime
from lib.space_repository import *
from lib.booking import *
from lib.booking_repository import *
from lib.user import User
from lib.user_repository import UserRepository
from flask_bcrypt import Bcrypt
from lib.space import *
# Create a new Flask app
app = Flask(__name__)
bcrypt = Bcrypt(app)

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')


@app.route('/', methods=['GET'])
def get_home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def post_signup():
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)

    # Get the fields from the request form
    email = request.form['email']
    password = request.form['password']
    password_confirmation = request.form['password_confirmation']

    # SQL query to check if email already exist as must be unique
    email_check = connection.execute('SELECT * from users WHERE email_address = %s', [email])
    # This if is checking to see if the sql query has found an instance of the email
    # If the email_check has found an entry then it will return an error message regarding email
    if email_check:
        email_error = "Email already registered"
        # Rendering template and returning the error message
        return render_template('home.html', email_error = email_error)
    # This else is if the entered email is not already in the database
    else:
        if len(password) == 0:
            password_error = "Password must not be blank"
            # This else happens when the password and password confirmation are not identical and returns errors on the sign up page
            return render_template('home.html', password_error = password_error)
        else:
            # hashed_password decodes and encrpytes the provided password
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            # The user is being created and added to the database with the hashed password
            user = User(None, email, hashed_password)
            # This checks to make sure password and password confirmation are identical
            if password == password_confirmation:
                # This checks the users email is not blank and password is valid
                if user.is_valid() == True:
                    # Save the user to the database
                    user_repository.create(user)
                    # Redirect to the login page for the user to sign in
                    return redirect('/login')
                else:
                    errors = user.generate_errors()
                    # This else happens when either the email or password is not valid and returns the errors on the sign up page
                    return render_template('home.html', errors = errors)
            else:
                password_error = "Passwords must be indentical"
                # This else happens when the password and password confirmation are not identical and returns errors on the sign up page
                return render_template('home.html', password_error = password_error)

@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    connection = get_flask_database_connection(app)

    # Get the fields from the request form
    email = request.form['email']
    password = request.form['password']

    # SQL commamnd to check if the email address is in the databse
    email_check = connection.execute('SELECT * from users WHERE email_address = %s', [email])
    # If email is found
    if email_check:
        # This is to check the password of the provided email
        password_check = email_check[0]['password']
        # is_valid is checking the provided password with the hashed pasword in the database
        is_valid = bcrypt.check_password_hash(password_check, password)
        # if the password provided and the hashed password are the same is_valid will return true and the user will be logged in.
        if is_valid == True:
            id = email_check[0]['id']
            # Redirects to the users spaces page using their id 
            return redirect(f"/{id}/spaces")
        else:
            password_error = "Incorrect password, please try again"
            # This else happens when the password is incorrect and returns arros on the login page
            return render_template('login.html', password_error = password_error)
    else:
        email_error = "Email not registered, please sign up"
        # This else happens if the email provided is not found in the database and returns error on login page
        return render_template('login.html', email_error = email_error)

@app.route('/about', methods=['GET'])
def get_about():
    return render_template('about.html')


@app.route('/1/spaces', methods=['GET'])
def get_spaces():
    return render_template('spaces.html')


@app.route('/1/spaces', methods=['POST'])
def get_spaces_available_spaces():
    connection = get_flask_database_connection(app)
    date = request.form['Pick A Date']
    datetimevar = datetime.strptime(str((date)), '%Y-%m-%d').date()
    spacerepo = SpaceRepository(connection)
    spaces = []
    available_list = spacerepo.in_window(datetimevar)
    for space in available_list:
        if spacerepo.is_available(space.id, datetimevar):
            spaces.append(space)
    return render_template('spaces_available.html', spaces = spaces, date = date)

@app.route('/1/book/<int:id>/', methods = ['POST'])
def book_date(id):
    connection = get_flask_database_connection(app)
    date = request.form['date']
    spacerepo = SpaceRepository(connection)
    space = spacerepo.find_by_id(id)
    return render_template('book.html', date = date, space = space)

@app.route('/1/current_book/<int:id>/', methods = ['POST'])
def make_booking(id):
    connection = get_flask_database_connection(app)
    date = request.form['date']
    current_booking = Booking(None, date, 1, id)
    bookrepo = BookingRepository(connection)
    bookrepo.create(current_booking)
    return redirect('/1/spaces')



@app.route('/1/spaces/new', methods=['GET'])
def get_create_space():
    return render_template('create_space.html')

@app.route('/1/spaces/new', methods=['POST'])

def create_a_space():
    connection = get_flask_database_connection(app)
    id = 1
    repo = SpaceRepository(connection)
    title = request.form['title']
    price = None
    if request.form['price_per_night']:
        price = float(request.form['price_per_night'])
    available_from = request.form['available_from']
    available_to = request.form['available_to']
    space = Space(None, title, price, available_from, available_to, id)
    if not space.is_valid():
        return render_template('create_space.html', errors=space.generate_errors())
    repo.create(space)
    return render_template('spaces.html', posted=True, space=space)


@app.route('/1/requests', methods=['GET'])
def get_requests():
    return render_template('requests.html')


@app.route('/1/requests', methods=['POST'])
def post_requests():
    return render_template('requests.html')


@app.route('/1/spaces/1', methods=(['GET']))  # change 1 to id later
def post_request_space():
    return render_template('single_space.html')


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
