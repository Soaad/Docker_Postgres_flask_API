
import time
import logging
from flask_caching import Cache
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

# DBUSER = 'postgres'
# DBPASS = 'postgres'
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'postgres'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'TestDB'

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
#Init App
app = Flask(__name__)
cache.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=POSTGRES_USER,  # DBUSER,
        passwd=POSTGRES_PASSWORD,  # DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'postgres'

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    address = db.Column(db.String(200))


def database_initialization_sequence():
    db.create_all()
    test_rec = Users(
        first_name='John',
        last_name='doe',
        age=20,
        address='los anglos')

    db.session.add(test_rec)
    db.session.commit()
    for i in range(1000000):
        user = Users()
        user.first_name = 'Firstname' + str(i)
        user.last_name = 'Lastname' + str(i)
        user.age = i
        user.address = 'Address' + str(i)
        db.session.add(user)
    db.session.commit()


@app.route('/users/', methods=['GET'])
def home():
    first_name_arg=request.args.get('first_name');#case not passed it will be None
    last_name_arg=request.args.get('last_name');
    age_arg=request.args.get('age');
    address_arg=request.args.get('address');
   # print("first_name_arg :"+first_name_arg)
   # print("last_name_arg :"+last_name_arg)
    #filtered_users=Users.query.limit(100).all()
    if first_name_arg is not None:
        filtered_users=Users.query.filter_by(first_name = first_name_arg)
    if last_name_arg is not None:
        filtered_users=Users.query.filter_by(last_name=last_name_arg)
    if age_arg is not None:
        filtered_users=Users.query.filter_by(age=age_arg)
    if address_arg is not None:
        filtered_users=Users.query.filter_by(address=address_arg)
    return render_template('show_filtered.html',filtered_users=filtered_users )


@app.route('/users_Json/', methods=['POST'])
def api_v2():
    request_date=request.get_json();
    if first_name  in request_date:
       first_name=request_date['first_name'];
    last_name=request_date['last_name'];
    age=request_date['age'];
    address=request_date['address'];
    print("first_name :"+first_name)
    print("last_name_arg :"+last_name)
    return render_template('show_filtered.html', users=Users.query.limit(100).all())

#run Server
if __name__ == '__main__':
    #if   Users.query.filter_by(age = 1).count() <= 0 :
    database_initialization_sequence()
    app.run(debug=True, host='0.0.0.0', port=8000)
