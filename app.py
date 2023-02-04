from flask import Flask, render_template, request, session, redirect, url_for, send_file
from datetime import datetime 
from functools import wraps
from flask_session import Session
from os import listdir
import os
  
app = Flask(__name__) 
app.secret_key = '*&%HGKHGHGJC&%&DXFCJCJG'
app.config['FILES_DIRECTORY'] = 'static/FILES/'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['password'] = 'kagebunshinojutsu007'

def check_login():
    print(session)
    if 'logged_in' not in session:
        return False
        
    if not session['logged_in']:
        
        return False
        
    return True

@app.route('/', methods=['GET', "POST"])
def login():
    session['logged_in'] = False
    if request.method == "POST":
        password = request.form['password']
        if password == app.config['password']:
            session['logged_in'] = True
        if not check_login():
            return redirect(url_for('login'))
        return redirect(url_for('upload'))
    return render_template("login.html")

@app.route('/upload', methods=['POST', 'GET']) 
def upload():
    if not check_login():
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['file']
        name = "".join(file.filename.split('.')[:-1])
        extension = file.filename.split('.')[-1]
        new_name = "{}-{}.{}".format(name, str(datetime.now()), extension)
        file.save(app.config['FILES_DIRECTORY']+new_name)
        return render_template("upload.html", message="☑️")
    return render_template("upload.html")


@app.route('/download', methods=['POST', 'GET'])
def download():
    if not check_login():
        return redirect(url_for('login'))

    files = []
    for file in listdir(app.config['FILES_DIRECTORY']):
        files.append(file)
    print(files)

    if request.method == 'POST':
        filename = request.form['filename']
        # uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
        # return send_from_directory(directory=uploads, filename=filename)
        path = app.config['FILES_DIRECTORY'] + filename
        return send_file(path, as_attachment=True)

    return render_template("download.html", files = files)


if __name__ =='__main__':  
    app.run(debug = True)  