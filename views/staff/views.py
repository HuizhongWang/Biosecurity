import base64
import os
import config
from flask import current_app, redirect, render_template, request, session, url_for, flash,g
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

# upload images format setting
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# check the format of the file is an image
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# get forestry data
def forestry_get(forestry_id):
    global detail_list,image_list
    connection = getCursor()
    connection.execute("""SELECT f.forestry_id,f.forestry_type,
                        case when f.present_in_nz = 1 then "yes" when f.present_in_nz=0 then "no" ELSE 'null' END
                        ,f.common_name,f.scientific_name,f.key_charac,f.biology,f.symptoms,i.images
                        FROM forestry f left join images i
                        on f.forestry_id = i.forestry_id
                        where i.show_p = 1 and f.forestry_id = %s""",(forestry_id,))
    detail_list = connection.fetchall()

    # select all images of the forestry
    connection.execute("""SELECT image_num,forestry_id,images FROM images where forestry_id = %s and show_p=0;""",(forestry_id,))
    image_list= connection.fetchall()

    
@staff_blu.route("/index",methods = ["GET","POST"])
def s_index():
    if session['userid'] and session['role'] == "staff" and session['status']== 1:
        connection = getCursor()
        # page setting
        page = request.args.get("page",1,type=int) 
        per_page = 10
        offset = (page -1) * per_page
        connection.execute("""SELECT f.forestry_id,f.forestry_type,
            case when f.present_in_nz = 1 then "yes" when f.present_in_nz=0 then "no" ELSE 'null' END
            ,f.common_name,i.images
            FROM forestry f left join images i
            on f.forestry_id = i.forestry_id
            where i.show_p = 1 order by f.forestry_id limit %s offset %s""",(per_page,offset,))
        guide_list = connection.fetchall()     

        connection.execute("select count(*) from forestry;")
        total = connection.fetchone()[0]   
        total_pages = total // per_page + (1 if total % per_page > 0 else 0)  # calculate the total pages

        if request.method == 'GET':    
            return render_template("staff/guide.html",guide_list=guide_list,page=page,total_pages=total_pages)
        else:
            # delete guide
            if request.values.get("del_guide") == "del_guide":
                forid= request.form.get("delid")
                connection.execute("delete from forestry where forestry_id=%s",(forid,))  
                flash("Delete successfully!","success")
            
            # upload images
            elif request.values.get("upload") == "upload":
                forid= int(request.form.get("forid"))
                if 'fileimg' not in request.files:
                    flash("No file part. Fail to add the image","danger")
                    return redirect(url_for('staff.s_index'))
                file_img = request.files.get("fileimg")
                if file_img.filename == '':
                    flash("No selected file. Fail to add the image","danger")
                    return redirect(url_for('staff.s_index'))
                if "fileimg" in request.files and allowed_file(file_img.filename):
                    file_img = request.files.get("fileimg")
                    file_name = file_img.filename
                    file_path = "/Users/doubleluo/Documents/GitHub/Biosecurity/static/imgdata/" + file_name
                    file_img.save(file_path)
                    connection.execute("select images from images where forestry_id=%s",(forid,))
                    images = connection.fetchall() 
                    if images[0][0]!=None:   # the forestry already have images
                        connection.execute("insert into images (forestry_id,images) values (%s,%s)", (forid,file_name,))
                    else:
                        connection.execute("update images set images=%s where forestry_id=%s", (file_name,forid,))
                    flash("File saved successfully","success")
                else:
                    flash('Invalid file type. Only PNG, JPG, JPEG, and GIF files are allowed.', 'danger')

            return redirect(url_for('staff.s_index'))
    else:
        return redirect(url_for('login'))


@staff_blu.route("/guide",methods = ["GET","POST"])
def s_guide():
        if session['userid'] and session['role'] == "staff" and session['status']== 1:
            connection = getCursor()
            # add guide
            if request.values.get("add") == "add":
                typ = request.form.get('group1')
                present = request.form.get("group2")
                common= request.form.get("common")
                scientific= request.form.get("sci")
                keys= request.form.get("key").strip()
                bio= request.form.get("biology").strip()
                symptoms= request.form.get("symptoms").strip()

                connection.execute("""insert into forestry  
                    (forestry_type,present_in_nz,common_name,scientific_name,key_charac, biology, symptoms) values
                    (%s,%s,%s,%s,%s,%s,%s)""",(typ,present,common,scientific,keys,bio,symptoms,))  
                
                connection.execute("select max(forestry_id) from forestry")
                forid = connection.fetchone()[0]
   
                flash("Add Forestry ID:{} successfully!".format(forid),"success")

                # upload images
                if 'fileimg' not in request.files:
                    connection.execute("""insert into images 
                        (forestry_id,show_p) values
                        (%s,%s)""",(forid,1))  
                    return render_template("staff/add_guide.html")
                file_img = request.files.get("fileimg")

                if file_img.filename == '':
                    connection.execute("""insert into images(forestry_id,show_p) values(%s,%s)""",(forid,1))  
                    return render_template("staff/add_guide.html")
                if "fileimg" in request.files and allowed_file(file_img.filename):
                    file_img = request.files.get("fileimg")
                    file_name = file_img.filename
                    file_path = "/Users/doubleluo/Documents/GitHub/Biosecurity/static/imgdata/" + file_name
                    file_img.save(file_path)
                    connection.execute("insert into images (forestry_id,images,show_p) values (%s,%s,1)", (forid,file_name,))
                else:
                    flash('But fail to add the file. Invalid file type. Only PNG, JPG, JPEG, and GIF files are allowed.', 'danger')
                    connection.execute("""insert into images(forestry_id,show_p) values(%s,%s)""",(forid,1))  
            
            return render_template("staff/add_guide.html")


@staff_blu.route("/detail",methods = ["GET","POST"])
def s_detail():   
    connection = getCursor()
    if session['userid'] and session['role'] == "staff" and session['status']== 1:
        forestry_id = request.args.get('forestry_id')   
        # forestry_get(forestry_id)
        if request.method == 'GET':                   
            forestry_get(forestry_id)
            return render_template("/staff/detail.html",detail_list=detail_list,image_list=image_list)    
        else:  
            # edit the detail 
            if request.values.get("edit") == "edit":
                forid= request.form.get("idnum") 
                common= request.form.get("common")
                scientific= request.form.get("scientific").strip()
                key= request.form.get("key").strip()
                bio= request.form.get("biology").strip()
                symptoms= request.form.get("symptoms").strip()
                type = request.form.get('group1')
                present = request.form.get("group2")
                connection.execute("""update forestry set 
                    forestry_type=%s,present_in_nz=%s,common_name=%s,scientific_name=%s,
                    key_charac=%s, biology=%s, symptoms=%s where forestry_id=%s""",(type,present,common,scientific,key,bio,symptoms,forid,))  
                flash("Update successfully!","success")

            # change picture
            elif request.values.get("save") == "save":
                img = request.form.get("img1")
                forid = request.form.get("forestry1")
                connection.execute("update images set show_p=0 where forestry_id=%s",(forid,))
                connection.execute("update images set show_p=1 where image_num=%s",(img,))
                flash("Change primary picture successfully!","success")

            # delete picture
            elif request.values.get("delimg") == "delimg":
                img = request.form.get("img")
                forid = request.form.get("forestry")
                connection.execute("delete from images where image_num=%s",(img,))
                flash("Delete picture successfully!","success")

            # get the data from database again after all change
            forestry_get(forid)
            return render_template("/staff/detail.html",detail_list=detail_list,image_list=image_list)          
    else:
        return redirect(url_for('login'))
      

@staff_blu.route("/profile",methods = ["GET","POST"])
def s_profile():
    hashing = g.hashing
    connection = getCursor()
    if session['userid'] and session['role'] == "staff" and session['status']== 1:
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
            if re.match(".*@.*",email) and re.match("^(?!00)\d{11}$",phone):
                connection.execute("update staff_admin set email=%s,phone=%s where staff_id=%s",(email,phone,user_id,)) 
            else:
                flash("Please check the format of email or phone number.","danger")
                return redirect(url_for('staff.s_profile'))
            
            # if modify password
            pwd_match = re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",password_c)
            if password_n != "" and password_c != "":
                if session['pwd']!= password:  # if the original password is not correct
                    flash("The original password is wrong.","danger")
                    return redirect(url_for('staff.s_profile'))
                else:
                    if password_n != password_c:  # 
                        flash("The second password input is incorrect. Please enter it again.","danger")  
                        return redirect(url_for('staff.s_profile')) 
                    else:
                        if pwd_match: 
                            n_hash = hashing.hash_value(password_c,salt="abc")
                            connection.execute("update staff_admin set pin=%s where staff_id=%s",(n_hash,user_id,))  
                            connection.execute("update users set pin=%s where staff_id=%s",(n_hash,user_id,))  
                            flash("Modify profile successfully.","success") 
                            return redirect(url_for('staff.s_profile'))
                        else:
                            flash("Please input your password in right format.","danger")    
                            return redirect(url_for('staff.s_profile')) 
            elif password_n != "" and password_c == "" or password_n == "" and password_c != "":
                flash("Please confirm your password.","danger")    
                return redirect(url_for('staff.s_profile')) 
            elif password != "":
                if session['pwd']!= password:    # if the original password is not correct
                    flash("The original password is wrong.","danger")
                    return redirect(url_for('staff.s_profile')) 
            elif password_n != password_c != "" and not re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",password_c):
                    flash("Please input your password in right format.","danger")    
                    return redirect(url_for('staff.s_profile')) 
            elif password_n == password_c != "" and not re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",password_c):
                    flash("Please input your password in right format.","danger")    
                    return redirect(url_for('staff.s_profile')) 
        
            flash("Modify profile successfully.","success") 
            return redirect(url_for('staff.s_profile'))
        
    else:
        return redirect(url_for('login'))


@staff_blu.route("/fprofile")
def fprofile():
    connection = getCursor()
    if session['userid'] and session['role'] == "staff" and session['status']== 1:
        # get the forester list
        connection.execute("SELECT * FROM forester where status_now = 1;")
        forester_list= connection.fetchall()
        return render_template("/staff/f_profile.html",forester_list=forester_list)
    else:
        return redirect(url_for('login'))

    

       