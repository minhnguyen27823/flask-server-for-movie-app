from flask import Flask
from flask import request
from mysql import connector
import pandas as pd

connection = connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="27082003",
    database="user_info"
)
app = Flask(__name__)
def check_email(email):
    query = "select * from user_info.account"

    df = pd.read_sql(query, con=connection)
    length = len(df["Email"])
    for i in range(length):
        if df["Email"][i] == email:
            return False
    return True
def check_username(username):
    query = "select * from user_info.account"

    df = pd.read_sql(query, con=connection)
    length = len(df["Username"])
    for i in range(length):
        if df["Username"][i] == username:
            return False
    return True

def check_account(username,password):
    query = "select * from user_info.account"


    df = pd.read_sql(query, con=connection)
    length = len(df["Username"])
    for i in range(length):
        if df["Username"][i] == username:
            if(df["Pass"][i] == password):
                return "Sign in success"
            else:
                return "Wrong password"
    return "No username found"

@app.route('/signin',methods=['POST'])
def signin():
    data = request
    username = data.args.get('Username')
    password = data.args.get('Pass')
    FirstName = data.args.get('FirstName')
    LastName = data.args.get('LastName')
    Email = data.args.get('Email')
    print( username, password, FirstName, LastName, Email)

    check_acc = check_account(username,password)


    return check_acc

@app.route('/signup',methods=['POST'])
def signup():

    data = request
    username=data.args.get('Username')
    password=data.args.get('Pass')
    FirstName=data.args.get('FirstName')
    LastName=data.args.get('LastName')
    Email=data.args.get('Email')
    print(username, password, FirstName, LastName,Email)
    mycursor = connection.cursor()

    log_return = ""
    check_mail = check_email(Email)

    if check_mail:
        check_user = check_username(username)
        if check_user == False:
            log_return = "Username is already registered"
        else:
            query = (
                " INSERT INTO user_info.account  (Username, Pass, FirstName, LastName, Email)  "
                f"VALUES ('{username}','{password}','{FirstName}','{LastName}','{Email}')")
            mycursor.execute(query)
            connection.commit()
            log_return = "Ok"
    else:
        log_return = "Email is already used"

    return log_return

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=8000, debug=True)