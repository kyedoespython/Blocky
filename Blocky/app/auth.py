from functools import wraps
from flask import redirect, url_for, flash, session


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("You must be logged in to access this page", "error")
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first", "error")
            return redirect(url_for("main.login"))

        from models import Users
        user = Users.query.get(session["user_id"])

        if not user or not user.is_admin:
            flash("Admins only", "error")
            return redirect(url_for("main.login"))

        return f(*args, **kwargs)
    return wrapper
