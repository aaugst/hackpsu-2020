import os
from flask import Flask, session, render_template, redirect, url_for, request, flash
from flask_socketio import SocketIO, send
import pyrebase
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import date
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET')
socketio = SocketIO(app)
firebaseConfig = {
    "apiKey": os.environ.get('FIREBASE_KEY'),
    "authDomain": "hackpsu-232d2.firebaseapp.com",
    "databaseURL": "https://hackpsu-232d2.firebaseio.com",
    "projectId": "hackpsu-232d2",
    "storageBucket": "hackpsu-232d2.appspot.com",
    "messagingSenderId": "329199728580",
    "appId": "1:329199728580:web:2074159a24c84db7711691"
  }
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()


@app.route("/login", methods = ["POST","GET"])
def login():
    if request.method == "POST":
        user_email = request.form["user_email"]
        user_password = request.form["user_password"]
        hashed = generate_password_hash(user_password)
        users = db.child('users').get()
        for user in users.each():
            user_val = user.val()
            if user_val['user_email']==user_email:
                if check_password_hash(user_val['hashed'],user_password):
                    session["user"] = user_val['user_name']
                    session["user_email"] = user_email
                    flash("Login in successfull!", "success")
                    return redirect(url_for('home'))
                else:
                    flash("wrong email or password", "error")
                    return redirect(url_for('login'))
        flash("wrong email or password", "error")
        return redirect(url_for("login"))
    else:
        return render_template("log-in.html")

@app.route("/signup", methods = ["POST","GET"])
def sign_up():
    if request.method == "POST":
        user_email = request.form["user_email_new"]
        user_name = request.form["user_name"]
        user_password = request.form["user_password_new"]
        hashed = generate_password_hash(user_password)
        db.child('users').push({"user_email":user_email,"user_name":user_name,"hashed":hashed})
        return redirect(url_for("login"))
    else:
        return render_template("sign-up.html")

@app.route("/logout")
def logout():
    session.pop("user",None)
    flash("Logged out", "error")
    return redirect(url_for("login"))
@app.route("/",methods=["POST","GET"])
def home():
    if "user" in session:
        user = session["user"]
        return render_template("home.html",user_name=user)
    else:
        return redirect(url_for("login"))

@app.route("/profile")
def profile():
    if "user" in session:
        user = session["user"]
        return render_template("profile.html")
    else:
        return redirect(url_for("login"))

@app.route("/chat")
def chat():
    if "user" in session:
        user = session["user"]
        return render_template("chat.html",user_name=user)
    else:
        return redirect(url_for("login"))

@socketio.on("message")
def message_handler(msg):
    send(msg,broadcast=True)

if __name__ == '__main__':
    app.run()