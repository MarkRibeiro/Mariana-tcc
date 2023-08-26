from flask import Flask, render_template, redirect, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__, template_folder="templates", static_folder="static")
client = MongoClient("localhost", 27017)
db = client["mari_tcc"]
global current_user
current_user = "none"

@app.route("/")
def start_page():
    return render_template("start.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    global current_user
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        user_doc = {
            "name": request.form["user_name"],
            "password": request.form["user_password"],
        }
        current_user = request.form["user_name"]
        user = db["users"].find_one(user_doc)
        if user == None:
            return redirect("/login")
        return redirect("/home")


@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    global current_user
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        user_doc = {
            "name": request.form["user_name"],
            "password": request.form["user_password"],
        }
        current_user = request.form["user_name"]
        user = db["users"].find_one(user_doc)
        if user == None:
            db["users"].insert_one(user_doc)
            return redirect("/home")
        return redirect("/signup")


@app.route("/home")
def home_page():
    global current_user
    return render_template("home.html", current_user = current_user)


app.run(port=5000, debug=True)
