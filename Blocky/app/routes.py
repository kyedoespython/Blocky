from flask import render_template, Blueprint, request, jsonify

from extensions import db
from models import User


main = Blueprint("main", __name__)


@main.route("/about")
def about_page():
    return render_template("about.html")

@main.route("/Join-Blocky")
def join_blocky():
    return render_template("signup.html")

@main.route("/send_signup", methods=["POST"])
def handle_signup():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    if not username:
        return "Missing username", 400
    if not password:
        return "Missing password", 400
    if not email:
        return "Missing email", 400

@main.route("/login")
def login():
    return render_template("login.html")

@main.route("/send_login")
def handle_login():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    #QUERY THE DATABASE FOR VERIFICATION