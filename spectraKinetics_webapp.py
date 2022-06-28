#
# Carl A. Fahlstrom
#
# Copyright 2016 
#

import os
from flask import Flask, render_templete, request, redirect, url_for
from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField
from werkzeug.utils import secure_filename

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

class 

class FileForm(Form):
	'''
	'''

	filename = StringField()
	fileContents = 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=[])
def index():
	'''
	'''


@app.route('/fileup', methods=['GET', 'POST'])
def upload_file():
    '''
    '''

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
