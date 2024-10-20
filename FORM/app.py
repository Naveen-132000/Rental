from flask import Flask, render_template, request, redirect, flash
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def send_email(name, form_email, phone, location, message):
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
        Message: {message}
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

@app.route('/', methods=['GET', 'POST'])
def contact():
    errors = {}
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        location = request.form['location']
        message = request.form['message']

        # Validation for name
        if not re.match(r'^[A-Za-z\s]+$', name):
            errors['name'] = 'Name should contain only alphabetic characters'

        # Validation for email
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            errors['email'] = 'Invalid email format'

        # Validation for phone (10 digits)
        if not re.match(r'^\d{10}$', phone):
            errors['phone'] = 'Phone number should be 10 digits long'

        # Validation for location (not empty)
        if len(location.strip()) == 0:
            errors['location'] = 'Location is required'

        # Validation for message (minimum length 10)
        if len(message) < 10:
            errors['message'] = 'Message should be at least 10 characters long'

        if not errors:
            if send_email(name, email, phone, location, message):
                flash('Your message has been sent successfully!', 'success')
            else:
                flash('Message saved, but failed to send an email. Please try again later.', 'error')

            return redirect('/')
        else:
            flash('There were errors in your submission. Please correct them.', 'error')

    return render_template('contact.html', errors=errors)

if __name__ == '__main__':
    app.run(debug=True)
