from flask import render_template, Blueprint, request, jsonify, redirect, flash, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps # USED FOR MAKING CUSTOM DECORATORS
from extensions import db
from models import Users
from auth import login_required

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
        flash("Missing username", "error")
        return redirect(url_for("main.join_blocky"))

    if not password:
        flash("Missing password", "error")
        return redirect(url_for("main.join_blocky"))

    if not email:
        flash("Missing email", "error")
        return redirect(url_for("main.join_blocky"))

    hashed_password = generate_password_hash(password)

    new_user = Users(
        username=username,
        password=hashed_password,
        email=email
    )

    db.session.add(new_user)
    db.session.commit()

    flash("Account created", "success")
    return redirect(url_for("main.login"))


@main.route("/login")
def login():
    return render_template("login.html")


@main.route("/send_login", methods=["GET", "POST"])
def handle_login():
    # If GET → show login page
    if request.method == "GET":
        return redirect(url_for("main.login"))

    # POST logic
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("Missing username or password", "error")
        return redirect(url_for("main.login"))
    
    user = Users.query.filter_by(username=username).first()

    if not user:
        flash("Invalid username", "error")
        return redirect(url_for("main.login"))

    if not check_password_hash(user.password, password):
        flash("Invalid password", "error")
        return redirect(url_for("main.login"))

    # KEEP USER LOGGED IN VIA SESSION
    session["user_id"] = user.id
    session ["username"] = user.username

    flash("Login successful!", "success")
    return redirect(url_for("main.configure"))

# END THE USER SESSION AND LOG THEM OUT OF THEIR ACCOUNT
@main.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "success")
    return redirect(url_for("main.login"))

@main.route("/configure")
@login_required
def configure():
    return render_template("configure.html")