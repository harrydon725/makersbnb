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


@app.route('/<int:id>/spaces', methods=['GET'])
def get_spaces(id):
    return render_template('spaces.html', userid = id)


@app.route('/<int:id>/spaces', methods=['POST'])
def get_spaces_available_spaces(id):
    connection = get_flask_database_connection(app)
    date = None
    if not request.form['Pick A Date']:
        date_error = "Date must not be empty"
        return render_template('spaces.html', date_error=date_error, userid = id)
    date = request.form['Pick A Date']
    datetimevar = datetime.strptime(str((date)), '%Y-%m-%d').date()
    spacerepo = SpaceRepository(connection)
    spaces = []
    available_list = spacerepo.in_window(datetimevar)
    for space in available_list:
        if spacerepo.is_available(space.id, datetimevar):
            spaces.append(space)
    return render_template('spaces_available.html', spaces = spaces, date = date, userid = id)

@app.route('/<int:id>/book/<int:id1>/', methods = ['POST'])
def book_date(id, id1):
    connection = get_flask_database_connection(app)
    date = request.form['date']
    spacerepo = SpaceRepository(connection)
    space = spacerepo.find_by_id(id1)
    return render_template('book.html', date = date, space = space, userid = id)

@app.route('/<int:id>/current_book/<int:id1>/', methods = ['POST'])
def make_booking(id, id1):
    connection = get_flask_database_connection(app)
    date = request.form['date']
    current_booking = Booking(None, date, id, id1)
    bookrepo = BookingRepository(connection)
    bookrepo.create(current_booking)
    return redirect(f'/{id}/spaces')

@app.route('/<int:id>/spaces/new', methods=['GET'])
def get_create_space(id):
    return render_template('create_space.html', userid = id)

@app.route('/<int:id>/spaces/new', methods=['POST'])
def create_a_space(id):
    connection = get_flask_database_connection(app)
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
    return render_template('spaces.html', posted=True, space=space, userid = id)


@app.route('/<int:id>/requests', methods=['GET'])
def get_requests(id):
    connection = get_flask_database_connection(app)
    userrepo = UserRepository(connection)
    # bookinglist = userrepo.find_bookings_with_name(id)
    return render_template('requests.html', userid = id)
    # connection = get_flask_database_connection(app)
    # user_repo = UserRepository(connection)
    # book_repo = BookingRepository(connection)
    # space_repo = SpaceRepository(connection)
    # book_info = book_repo.find_all_bookings_user(id)
    # list = user_repo.find_bookings_with_name(id)
    # requested_space = None
    # for booking in book_info:
    #     space_id = booking.spaceid
    #     # print(space_id)
    #     requested_space = space_repo.find_by_id(space_id)
    #     print (requested_space.title)
    # return render_template('requests.html', userid = id, bookings = list, space = requested_space)


# @app.route('/<int:id>/requests', methods=['POST'])
# def post_requests(id):
#     connection = get_flask_database_connection(app)
#     space_repo = SpaceRepository(connection)
#     book_repo = BookingRepository(connection)
#     book_info = book_repo.find_all_bookings_user(id)
#     # print (book_info)
#     for booking in book_info:
#         space_id = booking.spaceid
#         # print(space_id)
#         requested_space = space_repo.find_by_id(space_id)
#         print (requested_space.title)
#     # space_info = space_repo.find_by_id(book_info)
#     # print(space_info)
#     return render_template('requests.html', userid = id, bookings = book_info, space = requested_space.title)


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
