from flask import Flask, render_template, request, redirect, url_for, session
import plivo, sqlite3
import subprocess as sp

import utils

app = Flask(__name__)

# Initialize the SQLite database
conn = sqlite3.connect('sos_app.db')
cursor = conn.cursor()

# Create a table for user registrations
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_number TEXT NOT NULL,
        user_name TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Create a table for emergency contacts
cursor.execute('''
    CREATE TABLE IF NOT EXISTS emergency_contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contact_name TEXT NOT NULL,
        contact_number TEXT NOT NULL
    )
''')

conn.commit()
conn.close()


emergency_contacts = []

@app.route('/', methods=['GET', 'POST'])
def sos():
    if 'user_id' in session:
        user_id = session['user_id']

        conn = sqlite3.connect('sos_app.db')
        cursor = conn.cursor()

        # Retrieve sender number and emergency contacts based on user_id
        cursor.execute('SELECT sender_number FROM users WHERE id = ?', (user_id,))
        sender_number = cursor.fetchone()[0]

        cursor.execute('SELECT contact_name, contact_number FROM emergency_contacts WHERE user_id = ?', (user_id,))
        emergency_contacts = cursor.fetchall()

        conn.close()
        print(sender_number)
        print(emergency_contacts)
        return render_template('sos.html', user_id=user_id)
    if request.method == 'POST':
        sender_number = request.form['sender_number']
        sender_name = request.form['sender_name']
        contacts = request.form['emergency_contacts']
        emergency_contacts = [contact.strip() for contact in contacts.split(',')]
        dest_number = '<'.join(emergency_contacts)
        # You can now use sender_number and emergency_contacts for sending SOS messages or performing any other action
        city = sp.getoutput('curl ipinfo.io/city').strip().split('\n')[-1].strip()
        region = sp.getoutput('curl ipinfo.io/region').strip().split('\n')[-1].strip()
        loc = sp.getoutput('curl ipinfo.io/loc').strip().split('\n')[-1].strip()
        string = 'SOS from '+sender_name+ "(" +sender_number+ ")"+'\n City: '+city+'\n Region: '+region+'\n Coordinates: '+loc
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

    return render_template('sos.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission here
        # Retrieve username and password from the form

        user_number = request.form['user_number']
        password = request.form['password']

        # Check credentials and perform login logic here
        conn = sqlite3.connect('sos_app.db')
        cursor = conn.cursor()

        # Retrieve the user by user_number
        cursor.execute('SELECT * FROM users WHERE user_number = ?', (user_number,))
        user = cursor.fetchone()
        print(user)
        if user is not None and user[3] == password: 
            conn.close()
            return redirect(url_for('sos'))
        else:
            error = 'Invalid user number or password.'
            conn.close()
            return render_template('login.html', error=error)


    return render_template('login.html', user_logged_in=True)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle signup form submission here
        # Retrieve username, password, and confirm_password from the form

        user_number = request.form['user_number']
        user_name = request.form['user_name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Perform signup logic here
        if password == confirm_password:
            conn = sqlite3.connect('sos_app.db')
            cursor = conn.cursor()

            # Check if the user_number is already registered
            cursor.execute('SELECT * FROM users WHERE user_number = ?', (user_number,))
            existing_user = cursor.fetchone()

            if existing_user is None:
                # Insert the new user into the users table
                cursor.execute('INSERT INTO users (user_number, user_name, password) VALUES (?, ?, ?)', (user_number, user_name, password))
                conn.commit()
                conn.close()
                return redirect(url_for('login'))
            else:
                error = 'User number already registered.'
                conn.close()
                return render_template('signup.html', error=error)
        else:
            error = 'Passwords do not match.'
            return render_template('signup.html', error=error)

    return render_template('signup.html')

@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        contact_number = request.form['contact_number']

        # Add the new emergency contact to the list
        emergency_contacts.append(f"{contact_number}")

    return render_template('add_contact.html')

@app.route('/remove_contact', methods=['GET', 'POST'])
def remove_contact():
    if request.method == 'POST':
        contact_to_remove = request.form['remove_contact']

        # Remove the selected emergency contact from the list
        emergency_contacts.remove(contact_to_remove)

    return render_template('remove_contact.html')

if __name__ == '__main__':
    app.run(debug=True)

