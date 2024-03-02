import base64
import config
from flask import redirect, render_template, request, session, url_for, flash
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

# close database
def colseCursor():
     dbconn.close()
     connection.close()

@forester_blu.route("/index",methods = ["GET","POST"])
def f_index():
    if session['userid']:
        connection = getCursor()
        connection.execute("""SELECT f.forestry_id,f.forestry_type,
            case when f.present_in_nz = 1 then "yes" when f.present_in_nz=0 then "no" ELSE 'null' END
            ,f.common_name,i.images
            FROM forestry f left join images i
            on f.forestry_id = i.forestry_id
            where i.show_p = 1""")
        guide_get = connection.fetchall()
        # convert blob to base64 encodeing
        guide_list =[]
        for guide in guide_get:
            guide=list(guide)
            guide[4]= base64.b64encode(guide[4]).decode('ascii')
            guide_list.append(guide)       
        
        return render_template("forester/guide.html",guide_list=guide_list)

    else:
        return redirect(url_for('login'))
    

@forester_blu.route("/detail")
def f_detail():   
    connection = getCursor()
    if session['userid']:
        forestry_id = request.args.get('forestry_id') 
        connection.execute("""SELECT f.forestry_id,f.forestry_type,
            case when f.present_in_nz = 1 then "yes" when f.present_in_nz=0 then "no" ELSE 'null' END
            ,f.common_name,f.scientific_name,f.key_charac,f.biology,f.symptoms,i.images
            FROM forestry f left join images i
            on f.forestry_id = i.forestry_id
            where i.show_p = 1 and f.forestry_id = %s""",(forestry_id,))
        detail_get = connection.fetchall()
        # convert blob to base64 encodeing
        detail_list =[]
        for detail in detail_get:
            detail=list(detail)
            detail[8]= base64.b64encode(detail[8]).decode('ascii')
            detail_list.append(detail) 

        # select all images of the forestry
        connection.execute("""SELECT images FROM images where forestry_id = %s;""",(forestry_id,))
        image_get= connection.fetchall()
        image_list =[]
        for image in image_get:
            image=list(image)
            image[0]= base64.b64encode(image[0]).decode('ascii')
            image_list.append(image) 

        return render_template("/forester/detail.html",detail_list=detail_list,image_list=image_list)
    else:
        return redirect(url_for('login'))
      

@forester_blu.route("/profile",methods = ["GET","POST"])
def f_profile():
    connection = getCursor()
    if session['userid']:
        # get the profile from database
        user_id = session.get('user_id')
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

            # if change password,first check the original password,then check the new password and confirm password
            # if password != None:
            #     if session['pwd']== password: 
            #         flash("The original password is wrong.","danger")
            #     else:
            #         if password_n == password_c:
            #             n_hash = hashing.hash_value(password,salt="abc")
            #             connection.execute("update forester set pin=%s where forester_id=%s",(n_hash,get_id,))  
            #         else:
            #             flash("The confirm password is different from the new password.","danger")     
            
            # modify other info except password
            connection.execute("update forester set address=%s,email=%s,phone=%s where forester_id=%s",(address,email,phone,user_id,)) 
            flash("Modify profile successfully.","success") 
            return redirect(url_for('forester.f_profile'))
        
    else:
        return redirect(url_for('login'))


       