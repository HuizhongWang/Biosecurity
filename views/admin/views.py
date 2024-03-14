import base64
import config
from flask import redirect, render_template, request, session, url_for, flash,g
import re
import mysql
import mysql.connector
from . import admin_blu

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

    
@admin_blu.route("/index",methods = ["GET","POST"])
def a_index():
    if session['userid'] and session['role'] == "admin" and session['status']== 1:
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
        total_pages = total // per_page + (1 if total % per_page > 0 else 0)

        if request.method == 'GET':  
            return render_template("admin/guide.html",guide_list=guide_list,page=page,total_pages=total_pages)
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
                    return redirect(url_for('admin.a_index'))
                file_img = request.files.get("fileimg")

                if file_img.filename == '':
                    flash("No selected file. Fail to add the image","danger")
                    return redirect(url_for('admin.a_index'))
                
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
            
        return redirect(url_for('admin.a_index'))

    else:
        return redirect(url_for('login'))


@admin_blu.route("/guide",methods = ["GET","POST"])
def a_guide():
        if session['userid'] and session['role'] == "admin" and session['status']== 1:
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
                    connection.execute("""insert into images(forestry_id,show_p) values(%s,%s)""",(forid,1))  
                    return render_template("admin/add_guide.html")
                file_img = request.files.get("fileimg")
                if file_img.filename == '':
                    connection.execute("""insert into images(forestry_id,show_p) values(%s,%s)""",(forid,1))  
                    return render_template("admin/add_guide.html")
                if "fileimg" in request.files and allowed_file(file_img.filename):
                    file_img = request.files.get("fileimg")
                    file_name = file_img.filename
                    file_path = "/Users/doubleluo/Documents/GitHub/Biosecurity/static/imgdata/" + file_name
                    file_img.save(file_path)
                    connection.execute("insert into images (forestry_id,images,show_p) values (%s,%s,1)", (forid,file_name,))
                else:
                    flash('But fail to add the file. Invalid file type. Only PNG, JPG, JPEG, and GIF files are allowed.', 'danger')
                    connection.execute("""insert into images(forestry_id,show_p) values(%s,%s)""",(forid,1))  
            
            return render_template("admin/add_guide.html")


@admin_blu.route("/detail",methods = ["GET","POST"])
def a_detail():   
    connection = getCursor()
    if session['userid'] and session['role'] == "admin" and session['status']== 1:
        forestry_id = request.args.get('forestry_id')   
        # forestry_get(forestry_id)
        if request.method == 'GET':                   
            forestry_get(forestry_id)
            return render_template("/admin/detail.html",detail_list=detail_list,image_list=image_list)    
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
                print(type,forid,"ooooo")
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
            return render_template("/admin/detail.html",detail_list=detail_list,image_list=image_list)          
    else:
        return redirect(url_for('login'))
      

@admin_blu.route("/profile",methods = ["GET","POST"])
def a_profile():
    hashing = g.hashing
    connection = getCursor()
    if session['userid'] and session['role'] == "admin" and session['status']== 1:
        # get the profile from database
        user_id = session.get('userid')
        connection.execute("""SELECT * FROM staff_admin where staff_id= %s;""",(user_id,))
        staff_list= connection.fetchall()

        if request.method == "GET":
            return render_template("/admin/profile.html",staff_list=staff_list)
        else:
            department= request.form.get("depar")
            status= request.form.get("group1")
            position = request.form.get("a_ps")
            roles = request.form.get("a_role")
            first = request.form.get("a_first").strip()
            family = request.form.get("a_family").strip()
            email= request.form.get("a_email").strip()
            phone= request.form.get("a_phone").strip()
            date= request.form.get("a_date").strip()
            password= request.form.get("a_pass").strip()
            password_n= request.form.get("a_passn").strip()
            password_c= request.form.get("a_passc").strip()

            # modify other info except password
            if re.match(".*@.*",email) and re.match("^(?!00)\d{11}$",phone):
                connection.execute("""update staff_admin set roles=%s,first_name=%s,family_name=%s,
                    status_now=%s,email=%s,phone=%s,hire_date=%s,staff_position=%s,department=%s
                    where staff_id=%s""",(roles,first,family,status,email,phone,date,position,department,user_id,)) 
                connection.execute("update users set status_now=%s where staff_id = %s;",(status,user_id,))           
            else:
                flash("Please check the format of email or phone number.","danger")
                return redirect(url_for('admin.a_profile'))
            
            # if modify password
            pwd_match = re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",password_c)
            if password_n != "" and password_c != "":
                if session['pwd']!= password:    # if the original password is not correct
                    flash("The original password is wrong.","danger")
                    return redirect(url_for('admin.a_profile'))
                else:  # if the priginal password is correct
                    if password_n != password_c:  # if the confrim password is wrong 
                        flash("The second password input is incorrect. Please enter it again.","danger")   
                        return redirect(url_for('admin.a_profile')) 
                    else:  # if the confirm password is right
                        if pwd_match:  # check the format new password is right
                            n_hash = hashing.hash_value(password_c,salt="abc")
                            connection.execute("update staff_admin set pin=%s where staff_id=%s",(n_hash,user_id,))  
                            connection.execute("update users set pin=%s where staff_id=%s",(n_hash,user_id,))
                            flash("Modify profile successfully.","success") 
                            return redirect(url_for('admin.a_profile'))
                        else:
                            flash("Please input your password in right format.","danger")    
                            return redirect(url_for('admin.a_profile')) 
            elif password_n != "" and password_c == "" or password_n == "" and password_c != "":
                flash("Please confirm your password.","danger")    
                return redirect(url_for('admin.a_profile')) 
            elif password_n != password_c != "" and not re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",password_c):
                    flash("Please input your password in right format.","danger")    
                    return redirect(url_for('admin.a_profile')) 
            elif password != "":
                if session['pwd']!= password:    # if the original password is not correct
                    flash("The original password is wrong.","danger")
                    return redirect(url_for('admin.a_profile'))
            elif password_n == password_c != "" and not re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",password_c):
                    flash("Please input your password in right format.","danger")    
                    return redirect(url_for('admin.a_profile')) 

            flash("Modify profile successfully.","success") 
            return redirect(url_for('admin.a_profile'))
        
    else:
        return redirect(url_for('login'))


@admin_blu.route("/fprofile",methods = ["GET","POST"])
def f_profile():
    connection = getCursor()
    hashing = g.hashing
    if session['userid'] and session['role'] == "admin" and session['status']== 1:
        if request.method == "GET":
            # get the forester list
            connection.execute("SELECT * FROM forester where status_now = 1;")
            forester_list= connection.fetchall()
            return render_template("/admin/f_profile.html",forester_list=forester_list)
        else:
            # add forester
            if request.values.get("add_f") == "add_f":
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
                elif not re.match("^\d{1,11}$",phone):
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
                    connection.execute("insert into forester value(0,'forester',%s,%s,'1',%s,%s,%s,%s,%s)",(firstname,familyname,address,email,phone,date,pwd_hash,))
                    # get the forester id of the current register
                    connection.execute("select max(forester_id) from forester")
                    forester_id = connection.fetchone()[0]
                    connection.execute("insert into users(roles,forester_id,pin,status_now) values('forester',%s,%s,1)",(forester_id,pwd_hash,))
                    flash("Add successfully! Forester ID: {} ".format(forester_id),"success")
                
            # edit forester
            elif request.values.get("edit_f") == "edit_f":
                f_id = request.form.get("f_id")
                status= request.form.get("group1")
                first = request.form.get("f_first").strip()
                family = request.form.get("f_family").strip()
                address = request.form.get("f_add").strip()
                email= request.form.get("f_email").strip()
                phone= request.form.get("f_phone").strip()
                date= request.form.get("f_date").strip()
                password_n= request.form.get("f_passn").strip()
                password_c= request.form.get("f_passc").strip()

                # modify other info except password
                if re.match(".*@.*",email) and re.match("^(?!00)\d{11}$",phone):
                    connection.execute("""update forester set first_name=%s,family_name=%s,
                        status_now=%s,address=%s,email=%s,phone=%s,date_joined=%s 
                        where forester_id=%s""",(first,family,status,address,email,phone,date,f_id,))  
                    connection.execute("update users set status_now=%s where forester_id=%s",(status,f_id))
                else:
                    flash("Please check the format of email or phone number.","danger")
                    return redirect(url_for('admin.f_profile'))
                
                # if change password
                if password_n == password_c != "" and re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",password_c):
                    n_hash = hashing.hash_value(password_c,salt="abc")
                    connection.execute("update forester set pin=%s where forester_id=%s",(n_hash,f_id,))  
                    connection.execute("update users set pin=%s where forester_id=%s",(n_hash,f_id))
                elif password_n == password_c != "" and not re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",password_c):
                    flash("Please input your password in right format.","danger")    
                    return redirect(url_for('admin.f_profile')) 
                elif password_n != password_c != "" and not re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",password_c):
                    flash("Please input your password in right format.","danger")    
                    return redirect(url_for('admin.f_profile')) 
                
                flash("Modify the profile successfully.","success") 
            
            # delete forester
            elif request.values.get("del_f") == "del_f":
                f_id = request.form.get("id_del")
                connection.execute("update forester set status_now = 0 where forester_id=%s",(f_id,))  
                connection.execute("update users set status_now=0 where forester_id=%s",(f_id,))
                flash("Delete the forester successfully.","success") 

        return redirect(url_for('admin.f_profile')) 
    else:
        return redirect(url_for('login'))


@admin_blu.route("/sprofile",methods = ["GET","POST"])
def s_profile():
    connection = getCursor()
    hashing = g.hashing
    if session['userid'] and session['role'] == "admin" and session['status']== 1:
        if request.method == "GET":
            # get the staff list
            connection.execute("SELECT * FROM staff_admin where status_now = 1 and roles='staff';")
            staff_list= connection.fetchall()
            return render_template("/admin/s_profile.html",staff_list=staff_list)
        else:
            # add staff
            if request.values.get("add_s") == "add_s":
                # get input information
                position = request.form.get("a_ps")
                department= request.form.get("depar")
                familyname= request.form.get("familyname").strip()
                firstname= request.form.get("firstname").strip()
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
                elif not re.match("^\d{1,11}$",phone):
                    flash("Please input the phone number in right format.","danger")
                elif password != pass_con:
                    flash("The second password input is incorrect. Please enter it again.","danger")
                elif pass_con == "" or not re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",pass_con):
                    flash("Please input your password in right format.","danger")
                elif not date:
                    flash("Please input the joined date.","danger")
                    
                # insert into databases
                else:
                    pwd_hash = hashing.hash_value(pass_con,salt="abc")
                    connection.execute("insert into staff_admin value(0,default,%s,%s,1,%s,%s,%s,%s,%s,%s)",(firstname,familyname,email,phone,date,position,department,pwd_hash,))
                    # get the staff id of the current register
                    connection.execute("select max(staff_id) from staff_admin")
                    staff_id = connection.fetchone()[0]
                    connection.execute("insert into users(roles,staff_id,pin,status_now) values('staff',%s,%s,1)",(staff_id,pwd_hash,))
                    flash("Add successfully! Forester ID: {} ".format(staff_id),"success")
                
            # edit staff
            elif request.values.get("edit_s") == "edit_s":
                department= request.form.get("depar")
                status= request.form.get("group1")
                user_id = request.form.get("a_id")
                position = request.form.get("a_ps")
                roles = request.form.get("a_role")
                first = request.form.get("a_first").strip()
                family = request.form.get("a_family").strip()
                email= request.form.get("a_email").strip()
                phone= request.form.get("a_phone").strip()
                date= request.form.get("a_date").strip()
                password_n= request.form.get("a_passn").strip()
                password_c= request.form.get("a_passc").strip()

                # modify other info except password
                if re.match(".*@.*",email) and re.match("^(?!00)\d{11}$",phone):
                    connection.execute("""update staff_admin set roles=%s,first_name=%s,family_name=%s,
                        status_now=%s,email=%s,phone=%s,hire_date=%s,staff_position=%s,department=%s
                        where staff_id=%s""",(roles,first,family,status,email,phone,date,position,department,user_id,)) 
                    connection.execute("update users set status_now=%s where staff_id = %s;",(status,user_id,))   
                    connection.execute("update users set status_now=%s where staff_id=%s",(status,user_id))         
                else:
                    flash("Please check the format of email or phone number.","danger")
                    return redirect(url_for('admin.s_profile'))
                
                # if change password
                if password_n == password_c != "" and re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",password_c):
                    n_hash = hashing.hash_value(password_c,salt="abc")
                    connection.execute("update staff_admin set pin=%s where staff_id=%s",(n_hash,user_id,))  
                    connection.execute("update users set pin=%s where staff_id=%s",(n_hash,user_id,))
                elif password_n == password_c != "" and not re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",password_c):
                    flash("Please input your password in right format.","danger")    
                    return redirect(url_for('admin.s_profile')) 
                elif password_n != password_c != "" and not re.match("^(?=.*[a-zA-Z0-9!@#$%^&*()-+=])(?=.*[a-zA-Z0-9]).{8,30}$",password_c):
                    flash("Please input your password in right format.","danger")    
                    return redirect(url_for('admin.s_profile')) 

                flash("Modify profile successfully.","success") 
            
            # delete staff
            elif request.values.get("del_s") == "del_s":
                f_id = request.form.get("id_del")
                connection.execute("update staff_admin set status_now = 0 where staff_id=%s",(f_id,))  
                connection.execute("update users set status_now=0 where staff_id=%s",(user_id,))   
                flash("Delete the staff successfully.","success") 

        return redirect(url_for('admin.s_profile')) 
    else:
        return redirect(url_for('login'))

       