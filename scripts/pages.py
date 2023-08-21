from flask import Flask, render_template, redirect
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__, template_folder='templates', static_folder='static')
client = MongoClient("localhost", 27017)
db = client["mari_tcc"]

@app.route("/")
def start_page():
    return redirect("/login")

@app.route("/login")
def login_page():
    user = {"name":"Mari"}
    db["users"].insert_one(user)
    return "login"

@app.route("/home")
def home_page():
    return render_template("home.html")

app.run(port=5000, debug=True)