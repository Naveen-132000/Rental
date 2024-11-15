
    
    
from flask import Flask, render_template, request, redirect, url_for
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def send_email(name, form_email, phone, location, ):
    try:
        receiver_email = "darshan161211@gmail.com"
        password = "qnkk zaxf hrxr bfav"

        msg = MIMEMultipart()
        msg['From'] = form_email
        msg['To'] = receiver_email
        msg['Subject'] = "New Contact Form Submission"

        body = f"""
        New contact form submission:
        Name: {name}
        Email: {form_email}
        Phone: {phone}
        Location: {location}
        
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
@app.route('/logo')
def logo():
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
    location = request.form['location']
    

    # Validation for name
    if not re.match(r'^[A-Za-z\s]+$', name):
        return "Name should contain only alphabetic characters", 400

    # Validation for email
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return "Invalid email format", 400

    # Validation for phone (10 digits)
    if not re.match(r'^\d{10}$', phone):
        return "Phone number should be 10 digits long", 400

    # Validation for location (not empty)
    if len(location.strip()) == 0:
        return "Location is required", 400

    
   

    if send_email(name, email, phone, location, ):
        return redirect(url_for('thank_you'))  # Redirect to thank you page
    else:
        return "Message saved, but failed to send an email. Please try again later.", 500

@app.route('/thank_you', methods=['GET'])
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)