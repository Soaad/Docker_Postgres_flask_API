import time
import logging
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy


#DBUSER = 'postgres'
#DBPASS = 'postgres'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'TestDB'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=POSTGRES_USER,#DBUSER,
        passwd=POSTGRES_PASSWORD,#DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.logger.info(app.config['SQLALCHEMY_DATABASE_URI'] )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'postgres'


db = SQLAlchemy(app)


class users(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    address = db.Column(db.String(200))

    def __init__(self, first_name, last_name, age,address):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.address = address


def database_initialization_sequence():
    db.create_all()
    test_rec = users(
            'John',
            'doe',
            20,
            '123 Foobar Ave ,los anglos')
    
    db.session.add(test_rec)
    db.session.commit()
    for i in xrange(1000000):
        user = users()
        user.first_name = 'FirstNAME ' + str(i)
        user.last_name = 'LastNAME ' + str(i)
        user.age = i
        user.address = 'Address'+str(i)
        DBSession.add(user)
    db.session.commit()
    app.logger.info('database_initialization_sequence finished')

@app.route('/users/', methods=['GET'])
def home():
    return render_template('show_filtered.html', users=users.query.all())


if __name__ == '__main__':
    database_initialization_sequence()
    app.run(debug=True, host='0.0.0.0',port=8080)