import sqlite3

con = sqlite3.connect('mydatabase.db')
cur = con.cursor()
for row in cur.execute("SELECT * from todo_app;"):
    print(row[0])





