from flask import Flask, render_template, request, redirect, url_for
import plivo
import subprocess as sp

import utils

app = Flask(__name__)

emergency_contacts = []

@app.route('/', methods=['GET', 'POST'])
def sos():
    if request.method == 'POST':
        sender_number = request.form['sender_number']
        contacts = request.form['emergency_contacts']

        # Split the comma-separated contacts into a list
        emergency_contacts.extend([contact.strip() for contact in contacts.split(',')])
        dest_number = '<'.join(emergency_contacts)
        # You can now use sender_number and emergency_contacts for sending SOS messages or performing any other action
        city = sp.getoutput('curl ipinfo.io/city').strip().split('\n')[-1].strip()
        region = sp.getoutput('curl ipinfo.io/region').strip().split('\n')[-1].strip()
        loc = sp.getoutput('curl ipinfo.io/loc').strip().split('\n')[-1].strip()
        string = 'SOS from '+sender_number+'\n City: '+city+'\n Region: '+region+'\n Coordinates: '+loc
        print (string)
        client = plivo.RestClient(utils.plivo_id, utils.plivo_pass)
        response = client.messages.create(
            src=sender_number,
            dst=dest_number,
            text=string,
            url='https://0.0.0.0/sms_status/',
            )
        print(response)
        print(response.message_uuid)

    return render_template('sos.html', emergency_contacts=emergency_contacts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission here
        # Retrieve username and password from the form

        # Example:
        username = request.form['user_number']
        password = request.form['password']

        # Check credentials and perform login logic here

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle signup form submission here
        # Retrieve username, password, and confirm_password from the form

        # Example:
        username = request.form['user_number']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Perform signup logic here

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)

