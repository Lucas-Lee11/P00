'''
Forgotten Charger: Lewis Cass, Aryaman Goenka, Oscar Wang, Owen Yaggy
Softdev
P00: Cookie and Sessions Introduction
2021-10-29
time spent: 0.5
'''
import sqlite3
import db_builder
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'forgotten charger'

# Temporary username and password system
TEMP_USER = 'user'
TEMP_PASS = 'pass'

# Utility function to check if there is a session
def logged_in():
    return session.get('username') is not None

@app.route('/', methods=['GET'])
def landing():
    # Check for session existance
    if logged_in():
        return render_template('index.html')
    else:
        # If not logged in, show login page
        return render_template('intro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    method = request.method
    error = False
    # Check for session existance
    if method == 'GET':

        if logged_in():
            return render_template('index.html')
        else:
            # If not logged in, show login page
            return render_template('login.html', error=error)

    if method == 'POST':

        # Get information from request.form since it is submitted via post
        username = request.form['username']
        password = request.form['password']
        error = db_builder.login(username, password)

        if error:
            # If incorrect, give feedback to the user
            return render_template('login.html', error=error)
        else:
            # Store user info into a cookie
            session['username'] = username
            ##return redirect(url_for('landing'))
            return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    method = request.method
    error = True
    errormsg = ""
    # Check for session existence
    if method == "GET":
        if logged_in():
            return render_template('index.html')
            ##return render_template('confirm_add.html')
        else:
            # If not logged in, show login page
            return render_template('register.html', error=error, errmsg=errormsg)

    if method == "POST":
        new_username = request.form["new_username"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_username == "":
            error = True
            errormsg = "Error: No username entered!"
            return render_template("register.html", error=error, errmsg=errormsg)
        elif new_password == "":
            error = True
            errormsg = "Error: No password entered!"
            return render_template("register.html", error=error, errmsg=errormsg)
        elif confirm_password != new_password:
            error = True
            errormsg = "Error: Passwords do not match!"
            return render_template("register.html", error=error, errmsg=errormsg)

        error, errormsg = db_builder.signup(new_username, new_password)

        if error:
            return render_template("register.html", error=error, errmsg=errormsg)
        else:
            return render_template('intro.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():

    # Once again check for a key before popping it
    if logged_in():
        session.pop('username')

    # After logout, return to login page
    return redirect(url_for('landing'))

# For editing a particular story
@app.route('/<int:story_id>/edit')
def edit_story(story_id):
    return render_template('edit.html')

# For viewing a particular story
@app.route('/<int:story_id>')
def view_story(story_id):
    pass
    

# For handling submission of a new story
@app.route('/new', methods=['GET','POST'])
def add_story():

    method = request.method

    if method == 'GET':
        return render_template('new.html')


    if method == 'POST':

        title = request.form['title']
        story = request.form['story_text']
        confirm = request.form['sub1']
        if confirm == "Confirm":
            # make changes in database
            db_builder.new_story(title, story)
            print(title)
            print(story)
            print('changes attempted')
        message = ""
        if not title:
            message += "Please give your story a title. "
        if not story:
            message += "You cannot have an empty story. "
        if message:
            return render_template(
                'new.html',
                title = title,
                story = story,
                message = message
            )
        return render_template(
            'confirm_add.html',
        )

# Handles when a user visits a page without a route
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.debug = True
    app.run()
