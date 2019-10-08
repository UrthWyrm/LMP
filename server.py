from flask import Flask, render_template, request, redirect, flash, session
# from InstagramAPI import InstagramAPI
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re
import py_compile



py_compile.compile ('bot.py')


app = Flask(__name__)
# api = InstagramAPI("Login", "Password")
app.secret_key = 'puppybusiness'
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
##############################################################################
# Homepage
##############################################################################
@app.route('/LikeMyPics')
def index():
    return render_template('index.html')
##############################################################################
# Login Page
##############################################################################
@app.route('/LikeMyPics/login')
def login_page():
    return render_template('login.html')

# ###########################################################################
# Checking To See If Email Is Taken
# ###########################################################################
@app.route('/check-em', methods=['POST'])
def email():
    found = False
    mysql = connectToMySQL('like_my_pic')
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = { 'email': request.form['email'] }
    result = mysql.query_db(query, data)
    print('Hello')
    if result:
        found = True
    return render_template('partials/email.html', found=found)
############################################################################
# Registration Validation
############################################################################
@app.route("/registration", methods=['POST'])
def register():
    is_valid = True
    if len(request.form['fname']) < 1:
        is_valid = False
        flash("Please Enter a Valid First Name", "fnametoolittle")
    
    if len(request.form['lname']) < 1:
        is_valid = False
        flash("Please Enter a Valid Last Name", "lnametoolittle")

    if len(request.form['email']) < 1:
        is_valid = False
        flash("Please Enter a Valid Email", "emailtoolittle")
    
    else:
        mysql = connectToMySQL('like_my_pic')
        query = "Select * FROM users WHERE email=%(email)s"
        data = {
            'email': request.form['email']
        }
        result = mysql.query_db(query, data)
        if len(result) > 0:
            is_valid = False
            flash("This Email Is Already In Use", 'emailtoolittle')
    
    if len(request.form['pass']) <= 7:
        is_valid = False
        flash("Please Enter A Valid Password", 'pickpassword')
    
    if (request.form['cpass']) != request.form['pass']:
        is_valid = False
        flash("This Password Does Not Match", 'confpw')
    
    if not is_valid:
        return redirect("/")
    
    else:
        mysql = connectToMySQL('like_my_pic')
        pw_hash = bcrypt.generate_password_hash(request.form['pass'])
        print(pw_hash)
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, %(passW)s, NOW(), NOW());"
        data = {
            'fn': request.form['fname'],
            'ln': request.form['lname'],
            'em': request.form['email'],
            'passW': pw_hash
        }
        new_user_id = mysql.query_db(query, data)
        session['id'] = new_user_id
        session['first_name'] = request.form['fname']
        print(session['first_name'])
        print (session['id'])
        print(new_user_id)
        flash("You've Been Successfully Registered!", "Welcomein")
        return redirect("/dashboard/"+str(new_user_id))
############################################################################
# Registration Successful
############################################################################
@app.route("/success/<id>")
def registered(id):
    mysql = connectToMySQL('like_my_pic')
    query = "SELECT * FROM users WHERE id="+str(session['id'])
    users = mysql.query_db(query)
    fname = session['first_name']
    print(fname)
    return render_template("dashboard.html", users = users)
############################################################################
# Validating Log In
############################################################################
@app.route('/processlogin', methods=['POST'])
def logging():
    mysql = connectToMySQL('like_my_pic')
    query = 'SELECT * FROM users WHERE email = %(email)s'
    data = {
        'email': request.form['email']
    }
    user = mysql.query_db(query, data)
    if len(user) > 0:
        if bcrypt.check_password_hash(user[0]['password'], request.form['pass']):
            session['id'] = user[0]['id']
            return redirect('LikeMyPics/dashboard/'+str(user[0]['id']))

        else:

            flash('That Email And Password Does Not Match', 'passwordwrong')
            return redirect('/')
############################################################################
# Logged In
############################################################################
@app.route('/LikeMyPics/dashboard/<id>')
def Loggedin(id):
    print("Hello")
    if 'id' in session:
        mysql = connectToMySQL('like_my_pic')
        query = "SELECT * FROM users WHERE id="+str(session['id'])
        user_info = mysql.query_db(query)
        return render_template('dashboard.html', user_info = user_info)
    else:
        flash("You Are Not Logged In", 'loginhere')
        return redirect('/LikeMyPics')
############################################################################
# Google Login
############################################################################
@app.route('/logintogoogle')
def googleLoggedIn(id):
    print("Hello")
    if 'id' in session:
        mysql = connectToMySQL('like_my_pic')
        query = "SELECT * FROM users WHERE id="+str(session['id'])
        user_info = mysql.query_db(query)
        return render_template('dashboard.html', user_info = user_info)
    else:
        flash("You Are Not Logged In", 'loginhere')
        return redirect('/LikeMyPics')
############################################################################
# Instagram Login
############################################################################
@app.route('/LikeMyPics/dashboard.html?code=97106bf7de1449c3a495e2b05c87e74c')
def InstagramLogIn(id):
    print("Hello")
    if 'id' in session:
        mysql = connectToMySQL('like_my_pic')
        query = "SELECT * FROM users WHERE id="+str(session['id'])
        user_info = mysql.query_db(query)
        return render_template('dashboard.html', user_info = user_info)
    else:
        flash("You Are Not Logged In", 'loginhere')
        return redirect('/LikeMyPics')
############################################################################
# Starting Bot
############################################################################
@app.route('/exec')
def parse(name=None):
    import bot
    print("done")
    return render_template('dashboard.html',name=name)
##############################################################################
# Terms And Conditions
##############################################################################
@app.route('/LikeMyPics/terms')
def terms():
    return render_template('terms.html')
##############################################################################
# Privacy Policy
##############################################################################
@app.route('/LikeMyPics/privacy')
def privacy():
    return render_template('privacy.html')
##############################################################################
# Contacts
##############################################################################
@app.route('/LikeMyPics/contact')
def contacts():
    return render_template('contact.html')
############################################################################
# Log out
############################################################################
@app.route('/endsession/<id>')
def sessionover(id):
        session.clear()
        return redirect('/LikeMyPics')



if __name__ == ("__main__"):
    app.run(debug = True)