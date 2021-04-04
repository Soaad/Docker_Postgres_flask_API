
import time
import logging
from flask_caching import Cache
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa




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
        user=POSTGRES_USER,  
        passwd=POSTGRES_PASSWORD, 
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'postgres'
Users_PER_PAGE = 5

db = SQLAlchemy(app)
engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'] )

def table_exists(engine,name):
    ret = engine.dialect.has_table(engine, name)
    print('Table "{}" exists: {}'.format(name, ret))
    return ret
    
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
        user.first_name = 'Firstn' + str(i)
        user.last_name = 'Lastname' + str(i)
        user.age = i+1
        user.address = 'Address' + str(i+1)
        db.session.add(user)
    db.session.commit()

def get_list(**filters):
    print('users top 10 {}', Users.query.limit(10).all())
    page = request.args.get('page', 1, type=int)
    print('page  {}', page)
    #print('filters  {}', **filters)
    users = Users.query.filter_by(**filters).paginate(page=int(page),per_page=Users_PER_PAGE)
    return users



@app.route('/users/', methods=['GET'])
#@cache.cached()

def home():
    users=get_list(**request.args)
    page = request.args.get('page', 1, type=int)
    next_url = url_for('home', page=users.next_num) \
    if users.has_next else None
    prev_url = url_for('home', page=users.prev_num) \
    if users.has_prev else None
    return render_template('show_filtered.html',users=users.items ,next_url=next_url,
                           prev_url=prev_url)

#run Server
if __name__ == '__main__':
    #if not table_exists(engine,Users):
       # database_initialization_sequence()
    app.run(debug=True, host='0.0.0.0', port=8000)
