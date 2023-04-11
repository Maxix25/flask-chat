import sqlite3
from flask import Flask, render_template, session, redirect, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
db = sqlite3.connect("users.db", check_same_thread = False)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(username VARCHAR(20), password TEXT)")

socketio = SocketIO(app)

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]
        if (password == password_confirm):
            cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
            db.commit()
            return "Created user!"
    else:
        return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        results = cursor.execute("SELECT password FROM users WHERE (username = ?)", (username,)).fetchall()
        try:
            results[0]
            session["loggedin"] = True
            session["username"] = username
            return redirect("/")

        except IndexError:
            return "<h1>Invalid username or password!</h1>"
    else:
        return render_template("login.html")

@app.route("/")
def index():
    try:
        if session["loggedin"] == True:
            return render_template("index.html")
    except KeyError:
        return redirect("/login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@socketio.on("message")
def message(msg):
    if "username" in session:
        data = {"msg": msg, "username": session["username"]}
        emit("response", data, include_self = False, broadcast = True)
        print("Message emited: " + msg)

@socketio.on("send_msg")
def send_msg(msg):
    if "username" in session:
        emit("chat_msg", {"msg": msg, "username": session["username"]}, broadcast = True)
        print("Got message!")


if __name__ == "__main__":
    socketio.run(app, host = "0.0.0.0", debug = True)