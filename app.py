from flask import Flask, render_template, request, session, redirect, url_for
import os
import mysql.connector 
import sqlite3
from flask_login import UserMixin, login_user,LoginManager


app = Flask(__name__, static_url_path='/static')
app.debug = True
app.secret_key = 'your_secret_key'  #Replace 'your_secret_key' with a random and secure key
app.config['UPLOAD_FOLDER'] = 'amol/pgimages'
conn = sqlite3.connect('PG')

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mubbassir@123",
    database="PG"
)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

class User(UserMixin):
    def __init__(self, id):
        self.id = id


@app.route('/', methods=['GET', 'POST'])
def index():
    login_status = True  # Example login status

    if 'uname' in session:
        uname = session['uname']
        cursor = db.cursor()
        sql = "SELECT * FROM users WHERE first_name = %s"
        cursor.execute(sql, (uname,))
        user_data = cursor.fetchone()

        if request.method == 'POST':
            updated_first_name = request.form.get('fname')
            updated_lastname = request.form.get('lname')
            updated_email = request.form.get('email')
            updated_password = request.form.get('Pass')

            cursor = db.cursor()
            sql = "UPDATE users SET first_name = %s, last_name = %s, email = %s, password = %s WHERE first_name = %s"
            values = (updated_first_name, updated_lastname, updated_email, updated_password, uname)
            cursor.execute(sql, values)
            db.commit()

            return '''
            <script>
                alert("Profile Updated Successfully");
                window.location.href = "/";
            </script>
            '''

        return render_template('users/index.html', login_status=login_status, user_data=user_data)
    else:
        return render_template('users/index.html', login_status=login_status)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']
        pswd = request.form['password']
        cpass = request.form['confirm_password']

        cursor = db.cursor()
        check_query = "SELECT * FROM users WHERE first_name = %s"
        cursor.execute(check_query, (fname,))
        existing_user = cursor.fetchone()

        if existing_user:
            return '''
            <script>
                alert("User Already Exists");
                window.location.href = "/reg";
            </script>
            '''

        if pswd == cpass:
            sql = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
            values = (fname, lname, email, pswd)
            cursor.execute(sql, values)
            db.commit()
            return  '''
            <script>
                alert("REGISTERATION SUCCESSFULL");
                window.location.href = "/login";
            </script>
            '''
        else:
            return '''
            <script>
                alert("PLEASE ENTER CORRECT PASSWORD");
                window.location.href = "/reg";
            </script>
            '''

    return render_template('users/reg.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['first_name']
        pswd = request.form['Pass']

        cursor = db.cursor()
        sql = "SELECT * FROM users WHERE first_name = %s AND password = %s"
        values = (uname, pswd)
        cursor.execute(sql, values)
        user = cursor.fetchone()

        # Consume the result from the cursor
        cursor.fetchall()

        cursor.close()  # Close the cursor after fetching data

        if user:
            session['uname'] = user[1]  # Store the username in the session
            login_user(User(user[0]))
            session['logged_in'] = True
            session["uname"] = uname
            return '''
                <script>
                    alert(" Login Successful");
                    window.location.href = "/";
                </script>
            '''
        else:
            return '''
                <script>
                    alert("Invalid UserName or Password");
                    window.location.href = "/login";
                </script>
            '''

    return render_template('users/login.html')


@app.route('/ad_login', methods=['GET', 'POST'])
def ad_login():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        password = request.form.get('password')
        # Add your admin login logic here (e.g., check the username and password against a database)

        # For demonstration purposes, let's assume the username is "admin" and password is "password"
        if first_name == 'admin' and password == 'password':
            # Admin login successful, redirect to the admin dashboard
            return redirect('admin/ad_home')
        else:
            # Admin login failed, show an error message
            error_message = "Invalid credentials. Please try again."
            return render_template('users/ad_login.html', error_message=error_message)

    return render_template('users/ad_login.html')

# Owner Login
@app.route('/own_login', methods=['GET', 'POST'])
def own_login():
    if request.method == 'POST':
        uname = request.form['username']
        pswd = request.form['password']

        cursor = db.cursor()
        sql = "SELECT * FROM owner WHERE first_name = %s AND password = %s"
        values = (uname, pswd)
        cursor.execute(sql, values)
        user = cursor.fetchone()

        # Consume the result from the cursor
        cursor.fetchall()

        cursor.close()  # Close the cursor after fetching data

        if user:
            session['uname'] = user[1]  # Store the username in the session
            login_user(User(user[0]))
            session['logged_in'] = True
            session["uname"] = uname
            return '''
                <script>
                    alert(" Login Successful");
                    window.location.href = "/owner/own_home";
                </script>
            '''
        else:
            return '''
                <script>
                    alert("Invalid UserName or Password");
                    window.location.href = "/own_login";
                </script>
            '''

    return render_template('owner/own_login.html')

@app.route('/owner/own_home')
def own_home():
    return render_template('owner/own_home.html')  # You can create a separate template for owner's home page
@app.route('/owner/own_reg', methods=['GET', 'POST'])
def own_reg():
    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']
        pswd = request.form['password']
        cpass = request.form['confirm_password']

        cursor = db.cursor()
        check_query = "SELECT * FROM owner WHERE email = %s"
        cursor.execute(check_query, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return '''
            <script>
                alert("Owner Already Exists");
                window.location.href = "/owner/own_reg";
            </script>
            '''

        if pswd == cpass:
            sql = "INSERT INTO owner (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
            values = (fname, lname, email, pswd)
            cursor.execute(sql, values)
            db.commit()
            return  '''
            <script>
                alert("REGISTRATION SUCCESSFUL");
                window.location.href = "/own_login";
            </script>
            '''
        else:
            return '''
            <script>
                alert("PLEASE ENTER CORRECT PASSWORD");
                window.location.href = "/owner/own_reg";
            </script>
            '''

    return render_template('owner/own_reg.html')  # You can create a separate template for owner's registration page


@app.route('/owner/logout')
def own_logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/owner/owner_approvals')
def owner_approvals():
    cursor = db.cursor()
    sql = "SELECT * FROM book"
    cursor.execute(sql,)
    bookings = cursor.fetchall()

    if bookings:
        return render_template('owner/owner_approvals.html', bookings=bookings)

    # Handle the case when user data is not found or user is not logged in
    return render_template('owner/owner_approvals.html')

from flask import redirect
from werkzeug.utils import secure_filename
import json
@app.route('/owner/owner_upload', methods=['GET', 'POST'])
def owner_upload():
    if request.method == 'POST':
        food_types = json.dumps(request.form.getlist('food_types'))  # Convert the list to a JSON string
        parking = request.form['parking']
        state = request.form['state']
        city = request.form['City']
        oname = request.form['oname']
        price = request.form['Price']
        file1 = request.files['ophoto']
        filename = secure_filename(file1.filename)
        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file2 = request.files['iphoto']
        filename = secure_filename(file2.filename)
        file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


        cursor = db.cursor()
        sql = "INSERT INTO pg_details (food_types, parking, state, city,owner_name,price_per_month) VALUES (%s, %s,%s, %s, %s, %s)"  # Removed the trailing comma
        values = (food_types, parking, state, city,oname,price)
        cursor.execute(sql, values)

        db.commit()
        db.close()
        return '''
            <script>
                alert("PG Uploaded Successfully");
                window.location.href = "/owner/own_home";
            </script>
            '''
    return render_template('owner/owner_upload.html')
from flask import Blueprint
admin_bp = Blueprint('admin', __name__)

@app.route('/admin/ad_home')
def ad_home():
    total_users = 1000  # Example: count total users
    total_bookings = 500  # Example: count total bookings
    total_booked_pgs = total_bookings  # Count total booked PGs (assuming each booking is for a different PG)
    return render_template('admin/ad_home.html', total_users=total_users, total_bookings=total_bookings, total_booked_pgs=total_booked_pgs)
def get_all_users():
    cursor = db.cursor()
    sql = "SELECT * FROM users"
    cursor.execute(sql)
    users = cursor.fetchall()
    cursor.close()
    return users

@app.route('/admin/logout')
def ad_logout():
    session.clear()
    return redirect(url_for('index'))

def get_all_book():
    cursor = db.cursor()
    sql = "SELECT * FROM book"
    cursor.execute(sql)
    book = cursor.fetchall()
    cursor.close()
    return book

@app.route('/admin/ad_user')
def ad_user():
    users = get_all_users()
    return render_template('admin/ad_user.html', users=users)

@app.route('/admin/ad_book')
def ad_book():
    book = get_all_book()
    return render_template('admin/ad_book.html',book=book)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/room', methods=['GET'])
def room():
    try:
        # Connect to the MySQL database using the db dictionary
        cursor = db.cursor()

        # Execute the SQL query to retrieve room details
        sql = "SELECT * FROM pg_details"
        cursor.execute(sql)

        # Fetch all the room details
        room_data = cursor.fetchall()

        # Close the cursor
        cursor.close()

        # List all files in the "pgimages" folder
        image_folder = "amol/pgimages"
        image_files = os.listdir(image_folder)

        # Render the room.html template with the room_data and image_files
        return render_template('users/room.html', rooms=room_data, image_files=image_files)

    except mysql.connector.Error as err:
        # Handle the exception, log it, and provide an error message to the user
        error_msg = f"An error occurred: {err}"
        return render_template('users/room.html', error_msg=error_msg)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        uname = request.form['uname']
        npass = request.form['npass']
        cpass = request.form['cpass']

        if npass == cpass:
            cursor = db.cursor()
            cursor = db.cursor()
            sql = "UPDATE users SET PASSWORD = %s WHERE first_name = %s"
            values = (npass, uname)
            cursor.execute(sql, values)
            db.commit()
            return '''
            <script>
                alert("RESET PASSWORD SUCCESSFUL");
                window.location.href = "/login";
            </script>
            '''
        else:
            return '''
            <script>
                alert("PLEASE ENTER CORRECT PASSWORD")
                window.location.href = "users/forgot_password"
            </script>
            '''
    return render_template('users/forgot_password.html')

@app.route('/about_us')
def about_us():
    return render_template('users/Abt.html')

@app.route('/Cards')
def Cards():
    return render_template('users/Cards.html')

@app.route('/card1')
def card1():
    return render_template('users/card1.html')


@app.route('/card2')
def card2():
    return render_template('users/card2.html')


@app.route('/card3')
def card3():
    return render_template('users/card3.html')


@app.route('/card4')
def card4():
    return render_template('users/card4.html')

@app.route('/card5')
def card5():
    return render_template('users/card5.html')

@app.route('/card6')
def card6():
    return render_template('users/card6.html')

@app.route('/card7')
def card7():
    return render_template('users/card7.html')

@app.route('/card8')
def card8():
    return render_template('users/card8.html')

@app.route('/card9')
def card9():
    return render_template('users/card9.html')


# pg_details inforamation

# Function to create the pg_detail table
# def create_pg_detail_table():
#     with sqlite3.connect('pg_details.db') as connection:
#         cursor = connection.cursor()
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS pg_detail (
#                 id INTEGER PRIMARY KEY,
#                 name TEXT NOT NULL,
#                 address TEXT NOT NULL,
#                 capacity INTEGER NOT NULL,
#                 price INTEGER NOT NULL,
#                 available_rooms INTEGER NOT NULL,
#                 facilities TEXT NOT NULL,
#                 contact_number TEXT NOT NULL
#             )
#         ''')
#         connection.commit()

# # Function to insert sample data (optional, for demonstration)
# def insert_sample_data():
#     with sqlite3.connect('pg_details.db') as connection:
#         cursor = connection.cursor()
#         cursor.executemany('INSERT INTO pg_detail (name, address, capacity, price, available_rooms, facilities, contact_number) VALUES (%s, %s, %s, %s, %s, %s, %s)')
#         connection.commit()

# Route to display the admin view with PG details
@app.route('/')
def admin_view():
    with sqlite3.connect('pg_details.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM pg_detail')
        pg_details = cursor.fetchall()
    return render_template('admin_view.html', pg_details=pg_details)
    

# @app.route('/pg_details', methods=['POST','GET'])
# def pg_details():

@app.route('/book', methods=['POST','GET'])
def book():
    if request.method == 'POST':
        cursor = db.cursor()

        # Get the form data from the request
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        address = request.form['address']
        adhar_number = request.form['adhar_number']

        # Insert the form data into the MySQL table
        sql = "INSERT INTO book (name, phone_number, email, address, adhar_card_number) VALUES (%s, %s, %s, %s, %s)"
        values = (name, phone_number, email, address, adhar_number)
        cursor.execute(sql, values)

        # Commit the changes to the database
        db.commit()

        # Close the database connection
        cursor.close()

        return '''
                <script>
                    alert("PG Booked Successfully");
                    window.location.href = "/pay";
                </script>
            '''
    return render_template('users/book.html')

@app.route('/pay',methods=['POST','GET'])
def pay():
    if request.method=='POST':
        cursor = db.cursor() 
        name=request.form['Uname']
        UPI=request.form['upi']
        AMT=request.form['amt']
        sql = "INSERT INTO payment ( name,upi_id,amount) values(%s,%s,%s)"
        values=(name,UPI,AMT)
        cursor.execute(sql, values)
        db.commit()

        # Close the database connection
        cursor.close()
        return '''
                <script>
                    alert("Paid Successfully");
                     window.location.href = "/";
                </script>'''
    return render_template('users/pay.html')

if __name__ == '__main__':
    app.run()
