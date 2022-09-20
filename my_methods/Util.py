import os
import mysql.connector
from my_methods.logger import log
from datetime import datetime
import yaml
date=str(datetime.now())[:10]



def read_yaml_file(file_path)->dict:
    '''
    Read yaml file and return as dict 
    '''
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        print(e)

config_dir='config'
schema_filename='schema.yaml'
schema_filepath=os.path.join(config_dir,schema_filename)
config=read_yaml_file(schema_filepath)
try:
    ADMIN_PASS=config['admin_pass']
    ADMIN_NAME=config['admin_name']
    DB_USERNAME=config['db_username']
    DB_PASSWORD=config['db_pass']
    DB_HOST=config['db_host']
except Exception as e:
    print(e)

class Db:
    def __init__(self) -> None:
        self.db = mysql.connector.connect(host=DB_HOST ,user=DB_USERNAME, password=DB_PASSWORD)
        cursor=self.conn_cursor()
        cursor.execute('create database if not exists helpmecutmyclass')
        cursor.execute('use helpmecutmyclass')

    def conn_cursor(self):
        return self.db.cursor()
    
    def create_table(self,table_name,cols:list):
        cursor=self.conn_cursor()
        itter=0
        col=''
        for i in cols:
            itter+=1
            if itter ==1:
                col+=i
            else:
                col+=','+i
        try:
            print(f'CREATE TABLE IF NOT EXISTS {table_name} ({col})')
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({col})')
            self.Commit()
        except Exception as e:
                print(e)

    def insert_into(self,table_name,values:list):
        cursor=self.conn_cursor()
        value=str(values).replace('[','').replace(']','')
        print(f"INSERT INTO {table_name} VALUES ({value})")
        cursor.execute(f"INSERT INTO {table_name} VALUES ({value})")
        self.Commit()

    def Commit(self):
        self.db.commit()

    def Close(self):
        self.db.close()
    
    def check_login(self,username,userpass):
        cursor=self.conn_cursor()
        print(f"select password from logins where user_id = '"+username+"'")
        try:
            cursor.execute(f"select password from logins where user_id = '"+username+"'") 
            data=cursor.fetchall()
        except:
            return False , 'wrong user name or password'
        logins=False
        if len(data)!=0:
            for ele in data:
                if ele[0]==str(userpass):
                    print(userpass,ele[0])
                    logins=True
                    if logins:
                        return True , 'user name password validated succesfully'
                    else:
                        continue
            return logins , 'wrong user name or password'
        else:
            return logins , 'wrong user name or password'

    def check_for_first_entry(self,table_name,date,user_id):
        cursor=self.conn_cursor()
        cursor.execute(f"select * from {table_name} where dates={date} and user_id={user_id}")
        data=cursor.fetchall()
        if len(data)==0:
            return True
        else:
            return False

    def hour_list(self,table_name,date,username):
        cursor=self.conn_cursor()
        cursor.execute(f"select hour from {table_name} where dates='{date}'")
        data=cursor.fetchall()
        data_list=[]
        for ele in data:
            data_list.append(ele[0])
        log(username).info(f"hours added : {data_list}")
        return data_list
    
    def total_attendance(self,table_name):
        cursor=self.conn_cursor()
        cursor.execute(f"select present from {table_name} ")
        data=cursor.fetchall()
        data_list=[]
        for ele in data:
            data_list.append(int(ele[0]))
        if len(data)!=0:
            percentage=(len([x for x in data_list if x==1])/len(data))*100
            return f"{round(percentage,2)}%"
        else:
            return 0


    def subject_attendance(self,table_name,subject):
        cursor=self.conn_cursor()
        cursor.execute(f"select present from {table_name} where subject='{subject}'")
        data=cursor.fetchall()
        data_list=[]
        for ele in data:
            data_list.append(int(ele[0]))
        if len(data)!=0:
            percentage=(len([x for x in data_list if x==1])/len(data))*100
            return f"{round(percentage,2)}%"
        else:
            return 0

    def check_username(self,username):
        try:
            cursor=self.conn_cursor()
            cursor.execute("select password from logins where user_id='"+username+"'")
            data=cursor.fetchall()
            if len(data)==0:
                log(username).info(f"sign in succesfully")
                return True ,None
            else:
                for i in data:
                    password=i[0]
                return False,password
        except :
            return False,None

    def check_admin(self,username,userpass):
        print(username,userpass)
        if username==ADMIN_NAME and userpass==ADMIN_PASS:
            log(username).info('admin access granded')
            return True
        else:
            return False

    def del_day(self,username,date):
        cursor=self.conn_cursor()
        try:
            cursor.execute(f"DELETE FROM {username}_attendance WHERE dates='{date}'")
            log(username).info(f"exicute: [DELETE FROM {username}_attendance WHERE dates='{date}']")
        except Exception as e:
            return e
        self.Commit()

    def del_acc(self,username):
        cursor=self.conn_cursor()
        try:
            cursor.execute(f"delete from logins where user_id='{username}'")
            self.Commit()
            cursor.execute(f"drop table {username}_attendance")
            self.Commit()
            return 'success'
        except Exception as e :
            return str(e)
    def get_acc(self):
        cursor=self.conn_cursor()
        cursor.execute("select * from logins")
        data=cursor.fetchall()
        return data



def show_log(username,date):
    logfolder=os.path.join("log",username)
    logfilename="log_"+date+".log"
    logfilepath=os.path.join(logfolder,logfilename)
    with open (logfilepath,'r+') as logfile:
        data=logfile.readlines()
        print('done')
    return data

def del_log():
    logfolder1=os.path.join('log')
    dirs=os.listdir(logfolder1)
    for i in dirs:
        logfolder2=os.path.join('log',i)
        userlog=os.listdir(logfolder2)
        for j in userlog:
            d1 = datetime.strptime(j[4:14], "%Y-%m-%d")
            d2 = datetime.strptime(date, "%Y-%m-%d")
            f=d2-d1
            if int(f.days) >3 :
                del_path=os.path.join(logfolder2,j)
                os.remove(del_path)
                print('done')
    log('Menvar4077').info('log deletion complete')
    

            

