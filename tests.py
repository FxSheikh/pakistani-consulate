# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import sqlalchemy

from flask_sqlalchemy import SQLAlchemy
from flask_project import app, db
from applicant.models import *
from application.models import *


##############################################################################################

## Setup class for testing

##############################################################################################


class UserTest(unittest.TestCase):
    def setUp(self):
        db_username = app.config['DB_USERNAME']
        db_password = app.config['DB_PASSWORD']
        db_host = app.config['DB_HOST']
        self.db_uri = "mysql+pymysql://%s:%s@%s/" % (db_username, db_password, db_host)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DATABASE_NAME'] = 'test_database'
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri + app.config['DATABASE_NAME']
        engine = sqlalchemy.create_engine(self.db_uri)
        conn = engine.connect()
        conn.execute("commit")
        conn.execute("CREATE DATABASE " + app.config['DATABASE_NAME'])
        db.create_all()
        conn.close()
        self.app = app.test_client()
        
    def tearDown(self):
        db.session.remove()
        engine = sqlalchemy.create_engine(self.db_uri)
        conn = engine.connect()
        conn.execute("commit")
        conn.execute("DROP DATABASE " + app.config['DATABASE_NAME'])
        conn.close()


##############################################################################################

## Helper functions

##############################################################################################


    def register_user(self, first_name, middle_name, last_name, phone_number, email, password, password_confirm):
        return self.app.post('/register', data=dict(
            first_name = first_name,
            middle_name = middle_name,
            last_name = last_name,
            phone_number = phone_number,
            email = email,
            password = password,
            password_confirm = password_confirm
            ),
        follow_redirects = True)


    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email = email,
            password = password
            ),
        follow_redirects = True) 
        
    
    def logout(self):
        return self.app.get('/logout', follow_redirects = True)



#############################################################################################

## Testing functions

#############################################################################################


    def test_register_user(self):
        rv = self.register_user('John', 'Samuel', 'Wick', '12345678','john@example.com', 'test','test')
        assert 'Applicant registered' in str(rv.data)
        
    # create a test for registering user with same email/username        
    
    def test_login(self):
        self.register_user('John', 'Samuel', 'Wick', '12345678','john@example.com', 'test','test')
        rv = self.login('john@example.com','test')
        # print(rv.data)
        assert 'user john@example.com logged in' in str(rv.data)
        
    def test_logout(self):
        self.register_user('John', 'Samuel', 'Wick', '12345678','john@example.com', 'test','test')        
        self.login('john@example.com','test')
        rv = self.logout()
        # print(rv.data)
        assert 'User logged out' in str(rv.data)       
        
    def test_wrong_login(self):
        self.register_user('John', 'Samuel', 'Wick', '12345678','john@example.com', 'test','test')
        rv = self.login('wrong_email@test.com','wrong_password')
        # print(rv.data)
        assert 'Incorrect username and password' in str(rv.data)
        
    # test for creating application
    # test for uploading the images
    

if __name__ == '__main__':
    unittest.main()        