from flask import Flask, render_template, redirect, url_for
from flask_restful import Api, Resource, fields, marshal_with, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import datetime
import math
from datetime import date
from functools import wraps


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQL_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class TodoApp(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(200), primary_key=True)
    datecreate = db.Column(db.String, nullable=False)
    duedate = db.Column(db.String, nullable=False)
    remain = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'''TodoApp(todo={self.todo}) datecreate={self.datecreate} duedate={self.duedate} remain={self.remain})'''


resource_fields = {
    # 'id': fields.Integer,
    'todo': fields.String,
    'datecreate': fields.String,
    'duedate': fields.String,
    'remain': fields.String
}

#
# def my_connect(function):
#     global cur
#     con = sqlite3.connect('mydatabase.db', check_same_thread=False)
#     cur = con.cursor()
#
#     @wraps(function)
#     def wrapper(*args, **kwargs):
#         return function(*args, **kwargs)
#     return wrapper


def my_connect(func):
    global cur
    with sqlite3.connect('mydatabase.db', check_same_thread=False, timeout=10) as con:
        cur = con.cursor()

    def wrapper():
        val = func()
        db.session.commit()
        cur.close()
        db.session.close()
        con.close()
        return val
    return wrapper


@marshal_with(resource_fields)
@my_connect
@app.route('/')
def mainpage():
    # con = sqlite3.connect('mydatabase.db')
    # cur = con.cursor()
    db.create_all()
    updatepage()
    return render_template('main.html', content=cur)


def updatepage():
    for row in cur.execute("SELECT todo, duedate from todo_app;"):
        newdue = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') - datetime.datetime.now()
        newdue = str(newdue)
        if newdue[0] == '-':
            query = TodoApp.query.filter_by(todo=row[0]).first()
            db.session.delete(query)
        else:
            query = TodoApp.query.filter_by(todo=row[0]).first()
            pos = newdue.find('.')
            newdue = newdue[:pos]
            query.remain = newdue
    db.session.commit()
    db.session.close()





@marshal_with(resource_fields)
@my_connect
@app.route('/insert', methods=["POST"])
def insert():
    if request.method == "POST":
        todoinfo = request.form['todoinput']
        datecreated = datetime.datetime.now().replace(microsecond=0)
        duedate = request.form['dateex']
        duedate = datetime.datetime.strptime(duedate, '%Y-%m-%dT%H:%M')
        rem = str(duedate - datecreated)
        db.create_all()
        query = TodoApp(todo=todoinfo, datecreate=datecreated, duedate=duedate, remain=rem)
        db.session.add(query)
        db.session.commit()
        db.session.close()
        # con = sqlite3.connect('mydatabase.db')
        # cur = con.cursor()
        return redirect(url_for('mainpage'))
        # return render_template('main.html', content=cur)


@marshal_with(resource_fields)
@my_connect
@app.route('/delete/<string:ans>', methods=["GET", "POST"])
def delete(ans):
    query = TodoApp.query.filter_by(todo=ans).first()
    db.session.delete(query)
    db.session.commit()
    db.session.close()
    # con = sqlite3.connect('mydatabase.db')
    # cur = con.cursor()
    return redirect(url_for('mainpage'))
    # return render_template('main.html', content=cur)


if __name__ == "__main__":
    app.run(debug=True)


