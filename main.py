from flask import Flask, request
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader
(template_dir), autoescape=True)

app = Flask(__name__)

app.config["DEBUG"] = True

page_header = """
<!DOCTYPE = html>
<html lang = "en">
    <head>    
        <meta charset="UTF-5" />    
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />    
        <meta http-equiv="X-UA-Compatible" content="ie=edge" />    
        <title>Validation Example</title>    
        <link rel="stylesheet" href="/static/app.css" />  
    </head>
    <body>
"""
#template = jinja_env.get_template('welcome_message.html')
#template.render()


page_footer = """
    </body>
</html>
"""
reg_form = """
<form action="/register" id="form" method ='POST'>
    <h1>Register</h1>
    <label for= "username">Username</label>
    <input type ="text" name="username" id="username" value="{0}"/>
    <p class="error">{1}</p>
    <label for="password">Password</label>
    <input type="password" name="password" id="password" value="{2}"/>
    <p class="error">{3}</p>
    <label for="password">Enter Password Again</label>
    <input type="password" name="password_again" id="password_again" value="{4}"/>
    <p class="error">{5}</p>
    <label for="email">Email Address</label>
    <input type ="text" name="email" id="email" value="{6}"/>
    <p class="error">{7}</p>
    <button type ="submit">Submit</button>
</form>
"""

@app.route("/register", methods=['POST'])
def register():
    username = cgi.escape(request.form['username'])
    password = cgi.escape(request.form['password'])
    password_again = cgi.escape(request.form['password_again'])
    email = cgi.escape(request.form['email'])

    usernameError = ""
    passwordError = ""
    password_againError = ""
    emailError = ""
    email_count = 0

    if not username:
        print("No username")
        usernameError = "You Must Enter a User Name"
    if len(username) < 3 or len(username) > 20:
        usernameError = "You must enter a user name 3 characters or longer and shorter than 21" 
    for char in username:
        if char == " ":
            usernameError = "Your user name cannot contain a blank space"
    
    if not password:
        print("No password")
        passwordError = "You Must Enter a Valid Password"
    elif len(password) < 5:
        passwordError = "Your password must be at least 5 charaters long"
        password = ""
    else:
        num_in_password = False
        for x in password:
            if x.isdigit():
                num_in_password = True
        if not num_in_password:
            passwordError = "Your password must contain at least one number"
            password = ""
    for char in password:
        if char == " ":
            passwordError = "Your password cannot contain a blank space"
            password = ""
    if not password_again:
        password_againError = "You must re-enter your password"
    if password != password_again:
        password_againError = "Your 2nd entry did not match your 1st password"
        password_again = ""
        password = ""

    if email:
        if len(email) < 3 or len(email) > 20:
            emailError = "Please enter a valid email address"
            password = ""
            password_again = ""
        for char in email:
            if char == "@":
               email_count += 2
            elif char == ".":
                    email_count += 3 
        if email_count != 5:
            emailError = "Please enter a valid email address" 
            password = ""
            password_again = ""
            
    if usernameError or passwordError or password_againError or emailError:
        results = page_header + reg_form.format(username, usernameError, password, passwordError, password_again, password_againError, email, emailError) + page_footer
        return results

    return "Welcome,  " +  username

@app.route("/")
def index():
    template = jinja_env.get_template('welcome_message.html')
    results = page_header + template.render() + page_footer
    return results

@app.route("/register", methods=['GET'])
def register_response():
    template = jinja_env.get_template('reg_form_page.html')
    response = page_header + template.render() + page_footer
    return response

app.run()
















