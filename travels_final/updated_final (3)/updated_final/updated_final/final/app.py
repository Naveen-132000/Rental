from flask import Flask, render_template, request, redirect, url_for
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="utls"
    )

# Function to send email
def send_email(name, form_email, phone, pickup, drop, pickup_date, drop_date, vehicle):

    try:
        receiver_email = "darshan161211@gmail.com"
        password = "qnkk zaxf hrxr bfav"

        msg = MIMEMultipart()
        msg['From'] = form_email
        msg['To'] = receiver_email
        msg['Subject'] = "New Booking Form Submission"

        body = f"""
        New booking form submission:
        Name: {name}
        Email: {form_email}
        Phone: {phone}
        Selected Vehicle: {vehicle}
        Pickup Location: {pickup}
        Drop Location: {drop}
        Pickup Date: {pickup_date}
        Drop Date: {drop_date}
        """
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(receiver_email, password)
        text = msg.as_string()

        server.sendmail(form_email, receiver_email, text)
        server.quit()

        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    vehicle = request.form['vehicle']
    pickup = request.form['pickup']
    pickup_date = request.form['pickup_date']
    drop = request.form['drop']
    drop_date = request.form['drop_date']

    # Validation for name
    if not re.match(r'^[A-Za-z\s]+$', name):
        return "Name should contain only alphabetic characters", 400

    # Validation for email
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return "Invalid email format", 400

    # Validation for phone (10 digits)
    if not re.match(r'^\d{10}$', phone):
        return "Phone number should be 10 digits long", 400

    # Validation for pickup and drop locations
    if len(pickup.strip()) == 0 or len(drop.strip()) == 0:
        return "Pickup and drop locations are required", 400

    # Validation for dates
    try:
        pickup_date = datetime.strptime(pickup_date, '%Y-%m-%d').date()
        drop_date = datetime.strptime(drop_date, '%Y-%m-%d').date()

        # Ensure pickup date is not after drop date
        if pickup_date > drop_date:
            return "Pickup date cannot be after the drop date.", 400
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD.", 400

    # Save to the database
    db = get_db_connection()
    cursor = db.cursor()
    
    query = """INSERT INTO contacts1 (name, email, phone, vehicle, pickup, pickup_date, drop_location, drop_date)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (name, email, phone, vehicle, pickup, pickup_date, drop, drop_date)
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()

    # Send email
    if send_email(name, email, phone, pickup, drop, pickup_date, drop_date, vehicle):

        return redirect(url_for('thank_you'))
    else:
        return "Message saved, but failed to send an email. Please try again later.", 500

@app.route('/thank_you', methods=['GET'])
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
