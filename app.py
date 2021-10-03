from flask import Flask, render_template, request, make_response, redirect
from tinydb import TinyDB, Query
from datetime import datetime
import bcrypt
logs_desc_db = TinyDB('logs_desc.json')
cred_db = TinyDB('credentials.json')

item = Query()
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/logs')
def logs():
    return render_template('logs.html', user_logs = logs_desc_db.all())

@app.route('/logs_writer')
def logs_writer():
    return render_template('logs_writer.html')

@app.route('/logs_writer_input', methods=['POST'])
def logs_writer_input():
    title = request.form['title']
    body = request.form['body']
    email = request.cookies.get('user_id')
    username = cred_db.search(item.Email == email)[0]['Username']
    time = str(datetime.now().time())
    entry = {"username": username, "title": title, "body": body, "time": time}
    logs_desc_db.insert(entry)
    return render_template('logs_writer.html', status="Log successfully stored")

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_inputs', methods=['POST'])
def login_inputs():
    email = request.form['email']
    password = request.form['password']
    if cred_db.search(item.Email == email) != []:        
        if bcrypt.checkpw(password, cred_db.search(item.Email == email)[0]['Password']):
            resp = make_response(redirect('profile'))
            resp.set_cookie('user_id', cred_db.search(item.Email == email)[0]['Email'])
            return resp
        else:
            return render_template('login.html', error = 'Invalid credentials')
    else:
        return render_template('login.html', error = 'Invalid credentials')

@app.route('/profile')
def profile():
    email = request.cookies.get('user_id')
    username = cred_db.search(item.Email == email)[0]['Username']

    user_logs_profile = logs_desc_db.search(item.username == username)
    print(user_logs_profile)

    return render_template('profile.html', email=email, username=username, user_logs_profile=user_logs_profile)

@app.route('/cookies')
def cookies():
    return render_template('cookies.html')

if __name__ == "__main__":
    app.run(debug=True, threaded=True)