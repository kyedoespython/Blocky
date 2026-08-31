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