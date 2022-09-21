
from datetime import datetime
from my_methods.Util import Db,show_log,del_log
from flask import Flask,render_template,request,redirect,url_for
from my_methods.logger import log


app=Flask(__name__)




@app.route('/',methods=['GET','POST'])
def home():
    
    db=Db()
    db.create_table(table_name='logins',cols=['user_id varchar','password varchar'])
    
    if request.method =='POST':
        global username
        username=str(request.form['loginuser'])

        global userpass
        userpass=str(request.form['loginpass'])
        table_name=username+'_attendance'
        

        login,message=db.check_login(username=username,userpass=userpass)
        

        if login:
            log(username).info('=========================login page===========================')
            log(username).info(f'dbconnected successfuly')
            log(username).info(f'login for {username} with password {userpass}')
            log(username).info(message)

            db.create_table(table_name=table_name,cols=['dates varchar','time varchar','subject varchar','hour int','present int'])
            log(username).info(f"table [{table_name}] created")
            db.Close()
            return redirect(url_for('attendance'))
        else:
            db.Close()
            return render_template('home.html',loginmessage=message)
    db.Close()
    return render_template('home.html',loginmessage='')
    


@app.route('/sign_in',methods=['GET','POST'])
def signin():

    if request.method =='POST':
        username=str(request.form['signinuser'])
        userpass=str(request.form['signinpass'])
        usercpass=str(request.form['signincpass'])

        if userpass==usercpass:
            try:
                db=Db()
                check_signin,_=db.check_username(username=username)
                if not check_signin:
                    raise ValueError
                else:
                    log(username).info(f"=========================sign in page======================")
                    log(username).info(f"user name password entered .")
                    log(username).info(f"password and conform password matched.")

                    db.insert_into(table_name='logins',values=[username,userpass])
                    log(username).info(f"sign in details saved succesfully.")
            except Exception as e:
                log(username).info(f"error in sign in")
                db.Close()
                return render_template('sign_in_page.html',signinmessage='user name already taken.')
            db.Close()
            return redirect(url_for('home'))
        else:
            log(username).info(f"passwords doesn't match")

            return render_template('sign_in_page.html',signinmessage="passwords doesn't match")

    return render_template('sign_in_page.html',signinmessage='')
        

@app.route('/attendance',methods=['POST','GET'])
def attendance():
    db=Db()
    try:
        user_id=username
        log(user_id).info(f"===========================loged in ==========================")
    except:
        db.Close()
        return redirect(url_for('home'))
    if request.method=='POST':
        try:
            logout=str(request.form['logedout'])
            if logout=='log_out':
                log(user_id).info(f"logged out succesfully")
                del user_id
                
                db.Close()
                return redirect(url_for('home'))
        except  Exception as e:
            log(user_id).info(f"Exception:{e}")

        hour=int(request.form['hour'])
        subject=str(request.form['subject'])   
        radio=str(request.form.get("Radio"))
        time=str(datetime.now())[11:19]
        date=str(datetime.now())[:10]
        log(user_id).info(f"attendance is marked [{hour,subject,radio,time,date}]")
        
        h_list=db.hour_list(table_name=user_id+'_attendance',date=date,username=user_id)
        log(user_id).info(f"{h_list}")
        if hour not in h_list and len(h_list)<7:   
                db.insert_into(table_name=user_id+'_attendance',values=[date,time,subject,hour,radio])
                log(user_id).info(f"values add to database succesfully.")
        else:
            if len(h_list)==7:
                log(user_id).info(f"attendance for every hour for today has already marked.")
                return "attendance for every hour for today is marked.\n\n if you have any quiry contact us : menvar007@gmail.com"
            else:
                log(user_id).info(f"attendance for the selected hour is marked.")
                return 'attendance for the selected hour is marked.'

        if len(h_list)==7:
            db.Close()
        del h_list
        
    return render_template('marking_page.html')

@app.route('/show_attendance',methods=['GET','POST'])
def show_attendance():
    db=Db()
    try:
        user_id=username
        log(user_id).info(f"===========================show attendance========================")
    except:
        db.Close()
        return redirect(url_for('home'))
    percetage=db.total_attendance(table_name=user_id+'_attendance')
    sub1_percentage=db.subject_attendance(table_name=user_id+'_attendance',subject='sub1')
    sub2_percentage=db.subject_attendance(table_name=user_id+'_attendance',subject='sub2')
    sub3_percentage=db.subject_attendance(table_name=user_id+'_attendance',subject='sub3')
    sub4_percentage=db.subject_attendance(table_name=user_id+'_attendance',subject='sub4')
    sub5_percentage=db.subject_attendance(table_name=user_id+'_attendance',subject='sub5')
    sub6_percentage=db.subject_attendance(table_name=user_id+'_attendance',subject='sub6')
    sub7_percentage=db.subject_attendance(table_name=user_id+'_attendance',subject='sub7')
    log(user_id).info(f"attendance shown as : total:[{percetage}] subject wise:[{sub1_percentage, sub2_percentage,sub3_percentage,sub4_percentage,sub5_percentage,sub6_percentage,sub7_percentage}]")
    db.Close()
    return render_template('show_attendance.html',
                            total_percentage=percetage,
                            sub1_percentage=sub1_percentage,
                            sub2_percentage=sub2_percentage,
                            sub3_percentage=sub3_percentage,
                            sub4_percentage=sub4_percentage,
                            sub5_percentage=sub5_percentage,
                            sub6_percentage=sub6_percentage,
                            sub7_percentage=sub7_percentage
                            )
@app.route('/admin',methods=['POST','GET'])
def admin():
    db=Db()
    try:
        user_id=username
        user_pass=userpass
        master=db.check_admin(username=user_id,userpass=user_pass)
    except Exception as e:
        print(e)
        db.Close()
        return 'you are not an admin1'
    if master:
        log('Menvar4077').info(f"=====================admin page ============================")
        if request.method=="POST":
            try:
                _user_id=request.form['get_password']
                if _user_id:
                    _,password=db.check_username(username=_user_id)
                    log('Menvar4077').info(f"password is retreved for {_user_id}")
                    return password
            except Exception as a:
                log('Menvar4077').info(f"password retrieve not used [error : {a}]")

                try:                   
                    _date=str(request.form['_date'])
                    _user_id=str(request.form['_user_name'])
                    db.del_day(username=_user_id,date=_date)
                    log('Menvar4077').info(f"deleted datas from data base of: {user_id} of date: {_date} successfully.")
                    return 'success'
                except Exception as b:
                    log('Menvar4077').info(f"date delete not used [error : {b}]")
                    try:
                        _user_id=str(request.form['del_acc_username'])
                        db.del_acc(username=_user_id)
                        log('Menvar4077').info(f"account of {_user_id} deleted success fully")
                        return 'success'
                        
                    except Exception as c:
                        log('Menvar4077').info(f"delete account not used [error : {c}]")
                        try: 
                            acc_info=request.form['get_acc']  
                            print(acc_info)   
                            if acc_info=='get_accounts':
                                data=db.get_acc()
                                log('Menvar4077').info(f"all account details are retreved.")
                                return render_template('adminpage.html',data_to_show=data)
                        except Exception as d:
                            log('Menvar4077').info(f"accounts infos not used [error : {d}]")
                            try:
                                _user_id=str(request.form['logofuser'])
                                _date=str(request.form['datelogofuser'])
                                print(_user_id,_date)
                                data=show_log(username=_user_id,date=_date)
                                for i in data:
                                    print(i)
                                return render_template('adminpage.html',data_to_show=data)
                            except Exception as e:
                                try:
                                    del_log_req=request.form['dellogs']
                                    if del_log_req:
                                        del_log()
                                        log('Menvar4077').info(f"logs deleted.")
                                except Exception as f:
                                    log('Menvar4077').info(f"logs deletion. [error : {f}]")
                                    print(f)
    else:
        return 'you are not an admin.'
                                    
                                    

    return render_template('adminpage.html')

if __name__=='__main__':

    app.run(debug=True)
