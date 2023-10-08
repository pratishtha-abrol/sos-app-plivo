# SOS Application
- [SOS Application](#sos-application)
    - [Github Link: https://github.com/pratishtha-abrol/sos-app-plivo](#github-link-httpsgithubcompratishtha-abrolsos-app-plivo)
    - [Introduction](#introduction)
    - [Design Overview](#design-overview)
      - [Application Structure:](#application-structure)
      - [Database Design:](#database-design)
    - [Instalation and Setup](#instalation-and-setup)
    - [Usage](#usage)
      - [Registering a User](#registering-a-user)
      - [Logging In](#logging-in)
      - [Adding Emergency Contacts](#adding-emergency-contacts)
      - [Sending SOS Messages](#sending-sos-messages)
    - [Security Considerations](#security-considerations)
    - [Future Enhancements](#future-enhancements)
    - [Conclusion](#conclusion)


### Github Link: [https://github.com/pratishtha-abrol/sos-app-plivo](https://github.com/pratishtha-abrol/sos-app-plivo)

### Introduction 

The SOS (Save Our Souls) Application is a web-based emergency assistance platform built using Flask, a Python web framework. It allows users to quickly send distress signals and notify a list of emergency contacts in case of an emergency situation. This documentation provides an overview of the application's design, its approach to solving the problem, and details on how to use it effectively.

### Design Overview 

#### Application Structure:
The SOS Application follows a Model-View-Controller (MVC) architectural pattern:

* Model: The application uses SQLAlchemy, an Object-Relational Mapping (ORM) library, to define and interact with the database. Two main models are used: User for user registrations and authentications, and EmergencyContact for storing emergency contact numbers.

* View: HTML templates are used for rendering the web pages. Templates include sos.html for the main SOS page, login.html for the login page, signup.html for the signup page, and navbar.html for the navigation bar.

* Controller: The application logic is defined in the app.py file, which includes route handlers for different functionalities such as user registration, login, adding emergency contacts, and sending SOS messages.


#### Database Design:

The application uses a SQLite database to store user data and emergency contact numbers. Two primary tables are defined:

* User: Stores user information, including a unique user number and a hashed password for authentication.

* EmergencyContact: Stores a list of emergency contact numbers.



### Instalation and Setup

To install and run the SOS Application, follow these steps:

1. Clone the repository from GitHub.
2. Create a virtual environment and activate it.
   ```python
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the required packages  
   ```python
   pip install -r requirements.txt
   ```
4. Configure the database URI in the app.py file. Replace the plivo authentication id and password.
5. Create the database tables using `flask db init`, `flask db migrate`, and `flask db upgrade`.
6. Run the Flask application using 
   ```python 
   python3 app.py
   ```


### Usage
#### Registering a User

    1. Access the application in your web browser.
    2. Click on the "Signup" link in the navigation bar.
    3. Enter your user number, name and password in the signup form.
    4. Click the "Signup" button to create a new user account.

#### Logging In

    1. Access the application in your web browser.
    2. Click on the "Login" link in the navigation bar.
    3. Enter your user number and password in the login form.
    4. Click the "Login" button to log in to your account.

#### Adding Emergency Contacts

    1. Log in to your account.
    2. On the main SOS page, enter your sender's number and a list of comma-separated emergency contacts in the form, in case not logged in. 
    3. Click the "Send SOS" button to store the emergency contacts in the database.

#### Sending SOS Messages

    1. Log in to your account.
    2. On the main SOS page click the "Send SOS" button to send emergency alerts to the stored contacts.
    3. In case not logged in, enter your sender's number, name and emergency contacts before clicking the "Send SOS" button.


### Security Considerations
1. Passwords are securely hashed using a strong hashing algorithm to protect user data.
2. User input is sanitized and validated to prevent SQL injection and other security vulnerabilities.
3. Proper authentication and authorization mechanisms are implemented to ensure secure access to user data.


### Future Enhancements
The SOS Application can be further improved with the following enhancements:

    1. Implementing two-factor authentication (2FA) for added security.
    2. Developing a similar mobile application and adding a shake trigger.
    3. Integrating with emergency services for real-time assistance.


### Conclusion
The SOS Application is a powerful tool for users to seek help during emergency situations. This documentation provides an understanding of its design, approach, and usage. By following the installation and usage instructions, users can register, log in, add emergency contacts, and send SOS messages to improve their safety and security. Future enhancements will continue to make the application more robust and efficient.
