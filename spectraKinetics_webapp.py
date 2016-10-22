#
# Carl A. Fahlstrom
#
# Copyright 2016 
#

from flask import Flask, render_templete
from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
# We'll just use SQLite here so we don't need an external database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = ''

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

class dataPoint (db.Model):
	'''
	'''
	
	pointId = db.Column(db.Interger, primary_key=True)
	xData = db.Column(db.Float)
	yData = db.Column(db.Float)

class FileForm(Form):
	'''
	'''

	filename = StringField()
	fileContents = 
