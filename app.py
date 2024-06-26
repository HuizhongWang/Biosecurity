from flask import Flask,flash,render_template,request,session,redirect,url_for,g
import re
from flask_hashing import Hashing
from datetime import datetime
import mysql.connector
import config 

from views.admin import admin_blu
from views.staff import staff_blu
from views.forester import forester_blu

app = Flask(__name__)
app.secret_key = '123456'
hashing = Hashing(app)

app.register_blueprint(admin_blu,url_prefix="/admin")
app.register_blueprint(staff_blu,url_prefix="/staff")
app.register_blueprint(forester_blu,url_prefix="/forester")

@app.before_request
def before_request():
    g.hashing = hashing

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
    return render_template("index/home.html")

@app.route("/register",methods = ["GET","POST"])
def register():
    connection = getCursor()
    if request.method == "POST":        
        # get input information
        familyname= request.form.get("familyname").strip()
        firstname= request.form.get("firstname").strip()
        address= request.form.get("address")
        email= request.form.get("email").strip()
        phone= request.form.get("phone").strip()
        date= request.form.get("date").strip()
        password= request.form.get("password").strip()
        pass_con= request.form.get("pass_confirm").strip()

        # check input information
        if familyname == "" or not re.match("^.{1,30}$",familyname):
            flash("Please input the family name (Not exceeding 30 letters).","danger")
        elif firstname == "" and not re.match("^.{0,30}$",firstname):
            flash("The family name should not exceed 30 letters. Please input again","danger")
        elif not re.match(".*@.*",email):
            flash("Please input the right email.","danger")
        elif not re.match("^(?!00)\d{11}$",phone):
            flash("Please input the phone number in right format.","danger")
        elif not address:
            flash("Please input your address.","danger")
        elif password != pass_con:
            flash("The second password input is incorrect. Please enter it again.","danger")
        elif pass_con == "" or not re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",pass_con):
            flash("Please input your password in right format.","danger")
        elif not date:
            flash("Please input the joined date.","danger")
            
        # insert into databases
        else:
            pwd_hash = hashing.hash_value(pass_con,salt="abc")
            connection.execute("insert into forester values(0,default,%s,%s,1,%s,%s,%s,%s,%s)",(firstname,familyname,address,email,phone,date,pwd_hash,))
            # get the forester id of the current register
            connection.execute("select max(forester_id) from forester")
            forester_id = connection.fetchone()[0]
            connection.execute("insert into users(roles,forester_id,pin,status_now) values('forester',%s,%s,1)",(forester_id,pwd_hash,))
            flash("Register successfully! Please remember your ID: {}, it will be used for login.".format(forester_id),"success")
            # return redirect(url_for("register"))

    return render_template("index/register.html")


@app.route("/login",methods = ["GET","POST"])
def login():
    connection = getCursor()
    # get the login info
    if request.method == 'POST' and 'userid' in request.form and 'pwd' in request.form:
        userid = int(request.form['userid'])
        userpwd = request.form['pwd']
        connection.execute('SELECT * FROM users WHERE forester_id = %s or staff_id = %s', (userid,userid,))
        user = connection.fetchone()

        # if the userid is existed
        if user is not None:
            password = user[3]  # database pwd
            if hashing.check_value(password, userpwd, salt='abc'): # if the userid and password match
                session['pwd']=userpwd
            # If account exists in accounts table 
            # Create session data, we can access this data in other routes
                if user[1]:
                    session['userid'] = user[1]
                    session['role'] = "forester"
                    session['status'] = user[4]
                    return redirect(url_for('forester.f_index'))
                elif user[2] and user[0]=="staff":
                    session['userid'] = user[2]
                    session['role'] = "staff"
                    session['status'] = user[4]
                    return redirect(url_for('staff.s_index'))
                elif user[2] and user[0]=="admin":
                    session['userid'] = user[2]
                    session['role'] = "admin"
                    session['status'] = user[4]
                    return redirect(url_for('admin.a_index'))
            else:
                #password incorrect
                flash('Incorrect password!',"danger")
        else:
            # Account doesnt exist or username incorrect
            flash('Incorrect ID number',"danger")

    return render_template("index/login.html")


@app.route("/logout")
def logout():
    session.pop("userid", None) 
    getCursor()
    colseCursor()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)