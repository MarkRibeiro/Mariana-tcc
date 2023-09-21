from flask import Flask, render_template, redirect, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json

app = Flask(__name__, template_folder="templates", static_folder="static")
client = MongoClient("localhost", 27017)
db = client["mari_tcc"]
global current_user
current_user = "none"

global current_user_password
current_user_password = "none"

achievemet_images = []

user_achievements = {
    "conquista_01": False,
    "conquista_02": False,
    "conquista_03": False,
    "conquista_04": False,
    "conquista_05": False,
    "conquista_06": False,
    "conquista_07": False,
    "conquista_08": False,
    "conquista_09": False,
    "conquista_10": False,
    "conquista_11": False,
    "conquista_12": False,
    "conquista_13": False,
    "conquista_14": False,
    "conquista_15": False,
    "conquista_16": False,
    "conquista_17": False,
    "conquista_18": False,
    "conquista_19": False,
    "conquista_20": False,
    "conquista_21": False,
    "conquista_22": False,
    "conquista_23": False,
    "conquista_24": False,
    "conquista_25": False,
    "conquista_26": False,
}


@app.route("/")
def start_page():
    return render_template("start.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    global current_user
    global current_user_password
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        user_doc = {
            "name": request.form["user_name"],
            "password": request.form["user_password"],
        }
        current_user = request.form["user_name"]
        current_user_password = request.form["user_password"]
        user = db["users"].find_one(user_doc)
        if user == None:
            return redirect("/login")
        return redirect("/achievements")


@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    global current_user
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        user_doc = {
            "name": request.form["user_name"],
            "password": request.form["user_password"],
            "achievements": user_achievements,
        }
        current_user = request.form["user_name"]
        current_user_password = request.form["user_password"]
        user = db["users"].find_one(user_doc)
        if user == None:
            db["users"].insert_one(user_doc)
            return redirect("/achievements")
        return redirect("/signup")


@app.route("/achievements")
def achievements_page():
    global current_user
    set_achievements()
    return render_template(
        "achievements.html", current_user=current_user, achievements=achievemet_images
    )


@app.route("/home", methods=["GET", "POST"])
def home_page():
    global current_user
    if request.method == "GET":
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
    return render_template("home.html", current_user=current_user)


@app.route("/counters", methods=["GET", "POST"])
def counters_page():
    global current_user
    match_doc = {
        "user": current_user,
        "ongoing": True,
    }
    match = db["matches"].find_one(match_doc)

    if request.method == "GET":
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


def set_achievements():
    global current_user
    global current_user_password
    achievemet_images.clear()

    user = db["users"].find_one(
        {"name": current_user, "password": current_user_password}
    )

    for key in user["achievements"]:
        image_name = key
        if user["achievements"][key] == True:
            image_name = "/static/" + image_name + "_ativada.png"
            achievemet_images.append(image_name)
        else:
            image_name = "/static/" + image_name + "_desativada.png"
            achievemet_images.append(image_name)


app.run(port=5000, debug=True)
