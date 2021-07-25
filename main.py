from flask import Flask, render_template, redirect, url_for, flash
from flask_restful import Api, Resource, fields, marshal_with, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import datetime


app = Flask(__name__)
app.secret_key = "super secret key"
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQL_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class TodoApp(db.Model):
    todo = db.Column(db.String(200), primary_key=True)
    datecreate = db.Column(db.String, nullable=False)
    duedate = db.Column(db.String, nullable=False)
    remain = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'''TodoApp(todo={self.todo}) datecreate={self.datecreate} duedate={self.duedate} remain={self.remain})'''


resource_fields = {
    'todo': fields.String,
    'datecreate': fields.String,
    'duedate': fields.String,
    'remain': fields.String
}


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
    db.create_all()
    updatepage()
    return render_template('main.html', content=cur)


def updatepage():
    for row in cur.execute("SELECT todo, duedate from todo_app;"):
        newdue = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') - datetime.datetime.now()
        newdue = str(newdue)
        if newdue[0] == '-':
            query = TodoApp.query.filter_by(todo=row[0]).first()
            flash(f'''A post was automatically deleted since it met the deadline '{row[0]}' ''', 'success')
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
    try:
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
        return redirect(url_for('mainpage'))
    except:
        flash(f'''Event already present. Wait for it to complete''', 'warning')
        return redirect(url_for('mainpage'))


@marshal_with(resource_fields)
@my_connect
@app.route('/delete/<string:ans>', methods=["GET", "POST"])
def delete(ans):
    query = TodoApp.query.filter_by(todo=ans).first()
    db.session.delete(query)
    db.session.commit()
    db.session.close()
    flash(f'''Event {ans} was marked as completed by User''', 'danger')
    return redirect(url_for('mainpage'))


if __name__ == "__main__":
    app.run(debug=True)


