from flask import Flask,flash,render_template,request,session,redirect,url_for
import re
from flask_hashing import Hashing
from datetime import datetime
import mysql.connector
import config
from datetime import datetime

app = Flask(__name__)
hashing = Hashing(app)
app.secret_key = '123456'

# connect database
def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=config.dbuser, \
    password=config.dbpass, host=config.dbhost, \
    database=config.dbname, autocommit=True,auth_plugin='mysql_native_password')
    dbconn = connection.cursor()
    return dbconn

# close database
def colseCursor():
     dbconn.close()
     connection.close()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register",methods = ["GET","POST"])
def register():
    connection = getCursor()
    # if request.method == "GET":  
        # get the forester id of the current register
    connection.execute("select max(forester_id) from forester")
    forester_id = int(connection.fetchone()[0])
    forester_id += 1
        
    if request.method == "POST":        
        # get input information
        familyname= request.form.get("familyname").strip()
        firstname= request.form.get("firstname").strip()
        address= request.form.get("address")
        email= request.form.get("email").strip()
        phone= request.form.get("phone").strip()
        password= request.form.get("password").strip()
        date= request.form.get("date").strip()

        # check input information
        if familyname == "" or not re.match("^.{1,30}$",familyname):
            flash("Please input the family name (Not exceeding 30 letters).","danger")
        elif firstname == "" and not re.match("^.{0,30}$",firstname):
            flash("The family name should not exceed 30 letters. Please input again","danger")
        elif not re.match(".*@.*",email):
            flash("Please input the right email.","danger")
        elif not re.match("^\d{1,11}$",phone):
            flash("Please input the phone number in right format.","danger")
        elif not address:
            flash("Please input your address.","danger")
        elif password == "" or not re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",password):
            flash("Please input your password in right format.","danger")
        elif not date:
            flash("Please input the joined date.","danger")
            
        # insert into database
        else:
            pwd_hash = hashing.hash_value(password,salt="abc")
            connection.execute("insert into forester value(0,'forester',%s,%s,'1',%s,%s,%s,%s,%s)",(firstname,familyname,address,email,phone,date,pwd_hash,))
            flash("Register successfully!","success")
        colseCursor()
        # return redirect(url_for("register"))
    return render_template("register.html",forester_id=forester_id)


@app.route("/login",methods = ["GET","POST"])
def login():
    connection = getCursor()
    if request.method == 'POST' and 'userid' in request.form and 'pwd' in request.form:
        userid = int(request.form['userid'])
        print(userid,type(userid))
        userpwd = request.form['pwd']
        connection.execute('SELECT * FROM users WHERE forester_id = %s or staff_id = %s', (userid,userid,))
        # check if the userid is existed
        id = connection.fetchone()
        print(id)
        if id is not None:
            password = id[3]  # database pwd
            if hashing.check_value(password, userpwd, salt='abc'):
            # If account exists in accounts table 
            # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['roles'] = id[0]
                if id[1]:
                    session['userid'] = id[1]
                else:
                    session['userid'] = id[2]
                # Redirect to home page
                return redirect(url_for('dashboard'))
            else:
                #password incorrect
                flash('Incorrect password!',"danger")
        else:
            # Account doesnt exist or username incorrect
            flash('Incorrect ID number',"danger")
    return render_template("login.html")


@app.route("/dashboard",methods = ["GET","POST"])
def dashboard():

    return render_template("dashboard.html")

if __name__ == '__main__':
    app.run(debug=True)