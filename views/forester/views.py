from flask import redirect, render_template, session, url_for
import mysql
import config 
import mysql.connector
from . import forester_blu

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

@forester_blu.route("/index")
def index():
    if session['userid']:
        connection = getCursor()
        connection.execute("""SELECT forestry_id,forestry_type,present_in_nz,common_name,image_num
            FROM forestry""")
        guide_list = connection.fetchall()
        return render_template("forester/guide.html",guide_list=guide_list)

    else:
        return redirect(url_for('login'))
      

# @forester_blu.route("/profile")
# def f_profile():
#     if session['userid']:
#         return render_template("/forester/profile.html")
#     else:
#         return redirect(url_for('login'))

@forester_blu.route("/detail")
def f_detail():   
    if session['userid']:
        return render_template("/forester/detail.html")
    else:
        return redirect(url_for('login'))
       