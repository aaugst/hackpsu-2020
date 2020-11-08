import os
from flask import Flask, session, render_template, redirect, url_for, request
from flask_socketio import SocketIO, send
import pyrebase


# selecting the column in the database


app = Flask(__name__)


app.config['SECRET_KEY'] = "harambe"
socketio = SocketIO(app)
firebaseConfig = {
    "apiKey": "AIzaSyDkB_5swKCLTvjNiDTG_ahkknNy-9PgqEs",
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
        session["user"] = user_email
        return redirect(url_for("home"))
    else:
        return render_template("login.html")

@app.route("/")
def home():
    if "user" in session:
        user = session["user"]
        return render_template("home.html",user_name=user)
    else:
        return redirect(url_for("login"))

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@socketio.on("message")
def message_handler(msg):
    send(msg,broadcast=True)
if __name__ == '__main__':
    socketio.run(app)