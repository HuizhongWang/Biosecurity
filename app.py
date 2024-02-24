from flask import Flask,flash,render_template,request,session,redirect,url_for
import re
from datetime import datetime
import mysql.connector
import config
from datetime import datetime

app = Flask(__name__)

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



if __name__ == '__main__':
    app.run(debug=True)