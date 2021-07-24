# import sqlite3
#
# con = sqlite3.connect('mydatabase.db')
# cur = con.cursor()
# for row in cur.execute("SELECT * from todo_app;"):
#     print(row[0])


from functools import wraps


# def my_func(function):
#     val = function()
#     val = val.upper()
#     @wraps(function)
#     def wrapper(*args, **kwargs):
#
#         return function(*args, **kwargs)
#     return wrapper
#
#
# @my_func
# def func():
#     return "mahesh"
#
# print(func())



# import datetime
# from datetime import date
#
# today = datetime.datetime.now()
# duedate = datetime.datetime.strptime('2021 10 24', '%Y %m %d')
# print(today)
# print(duedate)
#
# print(duedate - today)


my_str = '23:46:20.349766'
print(my_str.rstrip('.'))
