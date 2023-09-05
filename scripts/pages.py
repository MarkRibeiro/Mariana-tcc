from flask import Flask, render_template, redirect, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json

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
    return render_template("home.html", current_user=current_user)


@app.route("/counters", methods=["GET", "POST"])
def counters_page():
    global current_user
    match_doc = {
        "user": current_user,
        "ongoing": True,
    }
    match = db["matches"].find_one(match_doc)
    if match == None:
        match_doc["counters"] = {
            "purple": 0,
            "pink": 0,
            "orange": 0,
            "yellow": 0,
            "green": 0,
        }
        db["matches"].insert_one(match_doc)

    if request.method == "GET":
        if match == None:
            return render_template(
                "counters.html",
                current_user=current_user,
                counters=match_doc["counters"],
            )
        else:
            return render_template(
                "counters.html", current_user=current_user, counters=match["counters"]
            )

    if request.method == "POST":
        new_values = {
            "$set": {
                "user": current_user,
                "ongoing": True,
                "counters": {
                    "purple": request.form["counterPurple"],
                    "pink": request.form["counterPink"],
                    "orange": request.form["counterOrange"],
                    "yellow": request.form["counterYellow"],
                    "green": request.form["counterGreen"],
                },
            }
        }
        db["matches"].update_one(match_doc, new_values)
        return redirect("/home")


app.run(port=5000, debug=True)
