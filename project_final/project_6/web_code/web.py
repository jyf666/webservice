from flask import Flask, request, flash, render_template
from flask import redirect, url_for, make_response
import datetime
import psutil
import sqlite3

app = Flask(__name__)
# 设置密匙
app.config['SECRET_KEY'] = 'hard to guess'
db_url = 'web.db'

# 主页判断


@app.route('/')
def hello():
    if not request.cookies.get('useremail') == None:
        return redirect(url_for("index"))
    else:
        return redirect(url_for('login'))

# 真正的主页


@app.route('/index', methods=['GET', 'POST'])
def index():
    if not request.cookies.get('useremail') == None:
        name = request.cookies.get('useremail')
        result = get_response()
        return render_template('index.html', name=name, result=result)
    else:
        return render_template('index.html', name=None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not request.cookies.get('useremail') == None:
        return redirect(url_for("index"))
    if request.method == 'GET':
        return render_template("login.html")
    useremail = request.form.get('useremail')
    password = request.form.get('password')
    login_rem = request.form.get('login_rem')
    create_table()
    user = select_user(useremail)
    if user:
        if user[1] == password:
            response = make_response(redirect(url_for('index')))
            if not login_rem == None:
                outdate = datetime.datetime.today() + datetime.timedelta(days=30)
                response.set_cookie('useremail', useremail, expires=outdate)
                return response
            response.set_cookie('useremail', useremail)
            return response
        else:
            flash('sorry,the password is wrong!')
    else:
        flash("sorry,user don't exist! please register one!")
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if not request.cookies.get('useremail') == None:
        return redirect(url_for("index"))
    if request.method == 'GET':
        return render_template("register.html")
    useremail = request.form.get('useremail')
    password = request.form.get('password')
    repassword = request.form.get('sec_password')
    if not password == repassword:
        flash('two passwords are not same !')
        return render_template("register.html")
    create_table()
    user = select_user(useremail)
    if user:
        flash('sorry,the user has existed!')
        return render_template("register.html")
    else:
        insert_user(useremail, password)
        flash("success!")
    return redirect(url_for("login"))


@app.route('/exit', methods=['GET'])
def exit():
    response = make_response(redirect(url_for("login")))
    if not request.cookies.get('useremail') == None:
        response.delete_cookie('useremail')
    return response


def create_table():
    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    sql = '''create table if not exists User (
        useremail text,
        password text)'''
    cursor.execute(sql)
    close(conn, cursor)


def insert_user(useremail, password):
    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    sql = '''insert into User (useremail, password) values ('%s','%s')''' % (
        useremail, password)
    cursor.execute(sql)
    conn.commit()
    close(conn, cursor)


def select_user(useremail):
    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    sql = '''select * from User where useremail = "%s"''' % useremail
    result = cursor.execute(sql).fetchone()
    close(conn, cursor)
    return result


def get_response():
    cpu_info = psutil.cpu_times()
    result = {"ram_total": int(psutil.virtual_memory().total / (1024 * 1024)),
              "ram_used": int(psutil.virtual_memory().used / (1024 * 1024)),
              "cpu_total": cpu_info,
              "cpu_user": psutil.cpu_percent(1),
              "cpu_logical": psutil.cpu_count(),
              "cpu_psy": psutil.cpu_count(logical=False)}
    return result


def close(conn, cursor):
    cursor.close()
    conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8002)
