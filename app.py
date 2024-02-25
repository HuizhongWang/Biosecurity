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
    if request.method == "GET":  
        # get the forester id of the current register
        connection.execute("select max(forester_id) from forester")
        forester_id = int(connection.fetchone()[0])
        forester_id += 1
        return render_template("register.html",forester_id=forester_id)
    else:       
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
            print(111111)
        elif not date:
            flash("Please input the joined date.","danger")
            
        # insert into database
        else:
            password = hashing.hash_value(password,salt="abc")
            connection.execute("insert into forester value(0,%s,%s,'active',%s,%s,%s,%s,%s)",(firstname,familyname,address,email,phone,date,password,))
            flash("Register successfully!","success")
        colseCursor()
        return redirect(url_for("register"))

@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)