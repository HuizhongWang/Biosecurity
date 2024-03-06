import base64
import config
from flask import redirect, render_template, request, session, url_for, flash,g
import re
import mysql
import mysql.connector
from . import staff_blu


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


# # get forestry data
# def forestry_get(forestry_id):
#     connection = getCursor()
    
@staff_blu.route("/index",methods = ["GET","POST"])
def s_index():
    if session['userid'] and session['role'] == "staff":
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
        
        return render_template("staff/guide.html",guide_list=guide_list)

    else:
        return redirect(url_for('login'))
    

@staff_blu.route("/detail",methods = ["GET","POST"])
def s_detail():   
    connection = getCursor()
    if session['userid'] and session['role'] == "staff":
        forestry_id = request.args.get('forestry_id')   
        # forestry_get(forestry_id)
        if request.method == 'GET':                   
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
            return render_template("/staff/detail.html",detail_list=detail_list,image_list=image_list)    
        else:    
            if request.values.get("edit") == "edit":
                forid= request.form.get("idnum")
                common= request.form.get("common")
                scientific= request.form.get("scientific").strip()
                key= request.form.get("key").strip()
                bio= request.form.get("biology").strip()
                symptoms= request.form.get("symptoms").strip()
                type = request.form.get('group1')
                present = request.form.get("group2")
                print(forid,88888888888888888)
                connection.execute("""update forestry set 
                    forestry_type=%s,present_in_nz=%s,common_name=%s,scientific_name=%s,
                    key_charac=%s, biology=%s, symptoms=%s where forestry_id=%s""",(type,present,common,scientific,key,bio,symptoms,forid,))  
                print(type,forid,"ooooo")
                flash("Update successfully!","success")
               
            elif request.values.get("delete") == "delete":
                forid= request.form.get("id")
                print(forid,9999999999999999999999)
                connection.execute("delete from forestry where forestry_id=%s",(forid,))  
                flash("Delete successfully!","success")
            
            connection.execute("""SELECT f.forestry_id,f.forestry_type,
                        case when f.present_in_nz = 1 then "yes" when f.present_in_nz=0 then "no" ELSE 'null' END
                        ,f.common_name,f.scientific_name,f.key_charac,f.biology,f.symptoms,i.images
                        FROM forestry f left join images i
                        on f.forestry_id = i.forestry_id
                        where i.show_p = 1 and f.forestry_id = %s""",(forid,))
            detail_get = connection.fetchall()

            # convert blob to base64 encodeing
            detail_list =[]
            for detail in detail_get:
                detail=list(detail)
                detail[8]= base64.b64encode(detail[8]).decode('ascii')
                detail_list.append(detail) 

            # select all images of the forestry
            connection.execute("""SELECT images FROM images where forestry_id = %s;""",(forid,))
            image_get= connection.fetchall()
            image_list =[]
            for image in image_get:
                image=list(image)
                image[0]= base64.b64encode(image[0]).decode('ascii')
                image_list.append(image) 

            # return redirect(url_for('staff.s_detail'))       
            return render_template("/staff/detail.html",detail_list=detail_list,image_list=image_list)          
    else:
        return redirect(url_for('login'))
      

@staff_blu.route("/profile",methods = ["GET","POST"])
def s_profile():
    hashing = g.hashing
    connection = getCursor()
    if session['userid'] and session['role'] == "staff":
        # get the profile from database
        user_id = session.get('userid')
        connection.execute("""SELECT * FROM staff_admin where staff_id= %s;""",(user_id,))
        staff_list= connection.fetchall()

        if request.method == "GET":
            return render_template("/staff/profile.html",staff_list=staff_list)
        else:
            email= request.form.get("email").strip()
            phone= request.form.get("phone").strip()
            password= request.form.get("password").strip()
            password_n= request.form.get("password_n").strip()
            password_c= request.form.get("password_c").strip()

            # modify other info except password
            if re.match(".*@.*",email) and re.match("^\d{1,11}$",phone):
                connection.execute("update staff_admin set email=%s,phone=%s where staff_id=%s",(email,phone,user_id,)) 
            else:
                flash("Please check the format of email or phone number.","danger")
                return redirect(url_for('staff.s_profile'))
            
            # if modify password
            pwd_match = re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",password_c)
            if password_n != "" and password_c != "":
                if session['pwd']!= password:    # if the original password is not correct
                    flash("The original password is wrong.","danger")
                    return redirect(url_for('staff.s_profile'))
                else:
                    if password_n != password_c:
                        flash("The twice password is different.","danger")   
                        return redirect(url_for('staff.s_profile')) 
                    else:
                        if pwd_match: 
                            n_hash = hashing.hash_value(password_c,salt="abc")
                            connection.execute("update staff_admin set pin=%s where staff_id=%s",(n_hash,user_id,))  
                        else:
                            flash("Please input your password in right format.","danger")    
                            return redirect(url_for('staff.s_profile')) 
            elif password_n != "" and password_c == "" or password_n == "" and password_c != "":
                flash("Please confirm your password.","danger")    
                return redirect(url_for('staff.s_profile')) 
        
            flash("Modify profile successfully.","success") 
            return redirect(url_for('staff.s_profile'))
        
    else:
        return redirect(url_for('login'))


@staff_blu.route("/fprofile")
def fprofile():
    connection = getCursor()
    if session['userid'] and session['role'] == "staff":
        # get the forester list
        connection.execute("SELECT * FROM forester;")
        forester_list= connection.fetchall()

    return render_template("/staff/f_profile.html",forester_list=forester_list)

       