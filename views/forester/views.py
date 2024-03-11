import base64
import config
import re
from flask import redirect, render_template, request, session, url_for, flash,g
import mysql
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


@forester_blu.route("/index",methods = ["GET","POST"])
def f_index():
    if session['userid'] and session['role'] == "forester" and session['status']== 1:
        connection = getCursor()
        connection.execute("""SELECT f.forestry_id,f.forestry_type,
            case when f.present_in_nz = 1 then "yes" when f.present_in_nz=0 then "no" ELSE 'null' END
            ,f.common_name,i.images
            FROM forestry f left join images i
            on f.forestry_id = i.forestry_id
            where i.show_p = 1""")
        guide_list= connection.fetchall()   
        
        return render_template("forester/guide.html",guide_list=guide_list)

    else:
        return redirect(url_for('login'))
    

@forester_blu.route("/detail")
def f_detail():   
    connection = getCursor()
    if session['userid'] and session['role'] == "forester" and session['status']== 1:
        forestry_id = request.args.get('forestry_id') 
        connection.execute("""SELECT f.forestry_id,f.forestry_type,
            case when f.present_in_nz = 1 then "yes" when f.present_in_nz=0 then "no" ELSE 'null' END
            ,f.common_name,f.scientific_name,f.key_charac,f.biology,f.symptoms,i.images
            FROM forestry f left join images i
            on f.forestry_id = i.forestry_id
            where i.show_p = 1 and f.forestry_id = %s""",(forestry_id,))
        detail_list = connection.fetchall()

        # select all images of the forestry
        connection.execute("""SELECT images FROM images where forestry_id = %s and show_p=0;""",(forestry_id,))
        image_list= connection.fetchall()
        return render_template("/forester/detail.html",detail_list=detail_list,image_list=image_list)
    else:
        return redirect(url_for('login'))
      

@forester_blu.route("/profile",methods = ["GET","POST"])
def f_profile():
    hashing = g.hashing
    connection = getCursor()
    if session['userid'] and session['role'] == "forester" and session['status']== 1:
        # get the profile from database
        user_id = session.get('userid')
        connection.execute("""SELECT * FROM forester where  forester_id= %s;""",(user_id,))
        profile_list= connection.fetchall()

        if request.method == "GET":
            return render_template("/forester/profile.html",profile_list=profile_list)
        else:
            address= request.form.get("address").strip()
            email= request.form.get("email").strip()
            phone= request.form.get("phone").strip()
            password= request.form.get("password").strip()
            password_n= request.form.get("password_n").strip()
            password_c= request.form.get("password_c").strip()

            # modify other info except password
            if re.match(".*@.*",email) and re.match("^\d{1,11}$",phone):
                connection.execute("update forester set address=%s,email=%s,phone=%s where forester_id=%s",(address,email,phone,user_id,)) 
            else:
                flash("Please check the format of email or phone number.","danger")
                return redirect(url_for('staff.s_profile'))    

            # if modify password
            pwd_match = re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",password_c)
            if password_n != "" and password_c != "":
                if session['pwd']!= password:    # if the original password is not correct
                    flash("The original password is wrong.","danger")
                    return redirect(url_for('forester.f_profile'))
                else:
                    if password_n != password_c:
                        flash("The second password input is incorrect. Please enter it again.","danger")   
                        return redirect(url_for('forester.f_profile')) 
                    else:
                        if pwd_match: 
                            n_hash = hashing.hash_value(password_c,salt="abc")
                            connection.execute("update forester set pin=%s where forester_id=%s",(n_hash,user_id,))  
                            connection.execute("update users set pin=%s where forester_id=%s",(n_hash,user_id,))
                        else:
                            flash("Please input your password in right format.","danger")    
                            return redirect(url_for('forester.f_profile')) 
            elif password_n != "" and password_c == "" or password_n == "" and password_c != "":
                flash("Please confirm your password.","danger")    
                return redirect(url_for('staff.s_profile')) 
            elif password != "":
                if session['pwd']!= password:    # if the original password is not correct
                    flash("The original password is wrong.","danger")
                    return redirect(url_for('forester.f_profile'))
            elif password_n != password_c != "" and not re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",password_c):
                    flash("Please input your password in right format.","danger")    
                    return redirect(url_for('admin.f_profile')) 
            
            flash("Modify profile successfully.","success") 
            return redirect(url_for('forester.f_profile'))
        
    else:
        return redirect(url_for('login'))


       