# flask-hub
This is a Flask app that handles accounts

Uses MySQL database 

# Note

To use you have to:

1-go to project/config.env

2-change the "PASSWORD" to your MySQL password at the DATABASE_URI variable

3-create a database named "flask" in MySQL

4-Run in terminal "flask --app run db init"

5-Run in terminal "flask --app run.py db migrate"

6-Run in terminal "flask --app run.py db upgrade"
