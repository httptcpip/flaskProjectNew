import distutils.config

from flask import Flask, render_template
import flask.config
import pymysql
import time

app = Flask(__name__)
app.config.from_object(flask.config)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/favicon.ico")
def icon():
    return render_template("resource/fan.ico")


@app.route("/loading.html")
def loading():
    return render_template('loading.html')


@app.route("/admin/<string:usrname>/<int:password>")
def admin(usrname, password):
    conn = pymysql.connect(host="localhost", db="homeworker", cursorclass=pymysql.cursors.DictCursor, user="root",
                           password="rootkg", charset="utf8")
    cur = conn.cursor()
    sql_sent1 = f"SELECT * FROM usr WHERE usrName = \"{usrname}\";"
    sql_sent2 = f"SELECT * FROM usr WHERE PASSWORD = {password};"
    print(sql_sent1)
    print(sql_sent2)
    cur.execute(sql_sent1)
    result = cur.fetchall()
    cur.execute(sql_sent2)
    result_1 = cur.fetchall()
    cur.close()
    conn.close()
    if result == () and result_1 == ():
        conn = pymysql.connect(host="localhost", db="homeworker", cursorclass=pymysql.cursors.DictCursor, user="root",
                               password="rootkg", charset="utf8")
        cur = conn.cursor()
        cur.execute("SELECT id FROM usr ORDER BY id;")
        result = cur.fetchall()
        if result != ():
            result = result[-1]
        else:
            result = 0
        print(F"INSERT INTO usr (id,usrName,op,PASSWORD) VALUES ({result + 1},\"{usrname}\",0,\"{str(password)}\"); ")
        cur.execute(
            F"INSERT INTO usr (id,usrName,op,PASSWORD) VALUES ({result + 1},\"{usrname}\",0,\"{str(password)}\"); ")
        # cur.submit()
        print(cur.fetchall())
        cur.close()
        conn.commit()
        conn.close()
        return render_template("admin.html", name=usrname, password=password)
    elif result != () and result_1 == ():
        return render_template("mistake.html")
    else:
        return render_template('admin.html', name=usrname, password=password)


@app.route("/submit/<string:usrname>/<int:password>/<int:hwc>")
def admin_back(usrname, password, hwc):
    conn = pymysql.connect(host="localhost", db="homeworker", cursorclass=pymysql.cursors.DictCursor, user="root",
                           password="rootkg", charset="utf8")
    cur = conn.cursor()
    print(F"SELECT * FROM usr WHERE usrName = \"{usrname}\" AND PASSWORD = {password}")
    cur.execute(F"SELECT * FROM usr WHERE usrName = \"{usrname}\" AND PASSWORD = {password};")
    reslut = cur.fetchall()
    conn.commit()
    conn.close()
    if reslut == ():
        return render_template("mistake.html")
    else:
        conn = pymysql.connect(host="localhost", db="homeworker", cursorclass=pymysql.cursors.DictCursor, user="root",
                               password="rootkg", charset="utf8")
        cur = conn.cursor()
        cur.execute("SELECT id FROM homework_record ORDER BY id;")
        subject_dict = {"1": "Chinese", "2": "Maths", "3": "English"}
    type_dict = {"1": "Homework book", "2": "Big Exercise Book", "3": "Note Book", "4": "Small", "5": "Other"}
    id = cur.fetchall()
    print(id)
    if id == ():
        id = 0
    else:
        id = id[-1]['id'] + 1
    print(
        f"INSERT INTO homework_record (ID,subject,type,usr,time) VALUES ({id},\"{subject_dict[str(hwc)[0:1]]}\",\"{type_dict[str(hwc)[1:2]]}\",\"{usrname}\",{time.time()})")
    cur.execute(
        f"INSERT INTO homework_record (ID,subject,type,usr,time) VALUES ({id},\"{subject_dict[str(hwc)[0:1]]}\",\"{type_dict[str(hwc)[1:2]]}\",\"{usrname}\",NOW());")
    conn.commit()
    cur.close()
    conn.close()
    return render_template('submitting.html', usrname=usrname, password=password, hwc=hwc)


if __name__ == '__main__':
    app.run(debug=True)
