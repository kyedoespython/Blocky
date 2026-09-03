from flask import render_template, Blueprint, request, jsonify, redirect, flash, url_for, session
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps # USED FOR MAKING CUSTOM DECORATORS
from extensions import db
from models import DatabaseProject, SchemaColumn, SchemaRelationship, SchemaTable, Users, UsersBackup1, UsersBackup2, UsersBackup3
from auth import admin_required, login_required

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
    _replicate_user(new_user)

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


@main.route("/admin-login", methods=["GET", "POST"])
@admin_required
def admin_login():
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form.get("username")).first()
        password = request.form.get("password")
        if not user or not user.is_admin or not password or not check_password_hash(user.password, password):
            flash("Invalid administrator credentials", "error")
            return redirect(url_for("main.admin_login"))
        session["user_id"] = user.id
        session["username"] = user.username
        session["is_admin"] = True
        return redirect(url_for("main.admin_page"))
    return render_template("admin_login.html")


@main.route("/admin")
@admin_required
def admin_page():
    return render_template("admin.html")


@main.route("/admin/query", methods=["POST"])
@admin_required
def admin_query():
    payload = request.get_json(silent=True) or {}
    sql = (payload.get("sql") or "").strip()
    target = payload.get("target", "main")
    if not sql:
        return jsonify({"error": "Enter a SQL query."}), 400
    engines = {"main": db.engine, "backup1": db.engines["backup1"], "backup2": db.engines["backup2"], "backup3": db.engines["backup3"]}
    if target == "all":
        results = {}
        for name, engine in engines.items():
            try:
                results[name] = _execute_query(engine, sql)
            except Exception as error:
                results[name] = {"error": str(error)}
        return jsonify({"target": "all", "results": results})
    if target not in engines:
        return jsonify({"error": "Unknown database target."}), 400
    try:
        return jsonify({"target": target, "results": _execute_query(engines[target], sql)})
    except Exception as error:
        return jsonify({"error": str(error)}), 400


def _execute_query(engine, sql):
    with engine.begin() as connection:
        result = connection.execute(text(sql))
        if result.returns_rows:
            return {"columns": list(result.keys()), "rows": [list(row) for row in result.fetchmany(500)]}
        return {"affected_rows": result.rowcount}


def _replicate_user(user):
    for backup_model in (UsersBackup1, UsersBackup2, UsersBackup3):
        db.session.add(backup_model(id=user.id, username=user.username, email=user.email,
                                    password=user.password, account_verified=user.account_verified,
                                    is_admin=user.is_admin, last_login=user.last_login))
    db.session.commit()

@main.route("/configure")
@login_required
def configure():
    project = DatabaseProject.query.filter_by(owner_id=session["user_id"]).order_by(DatabaseProject.id).first()
    if not project:
        project = DatabaseProject(name="Untitled database", owner_id=session["user_id"])
        db.session.add(project)
        db.session.commit()
    return render_template("configure.html", project=project)


@main.route("/api/schema", methods=["GET", "POST"])
@login_required
def schema_api():
    project = DatabaseProject.query.filter_by(owner_id=session["user_id"]).order_by(DatabaseProject.id).first()
    if request.method == "POST":
        payload = request.get_json(silent=True) or {}
        name = (payload.get("name") or "New table").strip()[:128]
        table = SchemaTable(name=name or "New table", project_id=project.id,
                            position_x=payload.get("position_x", 80), position_y=payload.get("position_y", 80))
        table.columns.append(SchemaColumn(name="id", data_type="INTEGER", is_primary_key=True, is_nullable=False))
        db.session.add(table)
        db.session.commit()
        return jsonify({"id": table.id, "name": table.name, "columns": _columns(table)}), 201

    return jsonify({
        "project": {"id": project.id, "name": project.name},
        "tables": [{"id": table.id, "name": table.name, "position_x": table.position_x,
                    "position_y": table.position_y, "columns": _columns(table)} for table in project.tables],
        "relationships": [{"id": relationship.id, "from_table_id": relationship.from_table_id,
                            "to_table_id": relationship.to_table_id, "from_column": relationship.from_column,
                            "to_column": relationship.to_column} for relationship in SchemaRelationship.query.join(
                                SchemaTable, SchemaRelationship.from_table_id == SchemaTable.id).filter(
                                    SchemaTable.project_id == project.id)]
    })


def _columns(table):
    return [{"id": column.id, "name": column.name, "data_type": column.data_type,
             "is_primary_key": column.is_primary_key, "is_nullable": column.is_nullable} for column in table.columns]


@main.route("/api/schema/table/<int:table_id>", methods=["PATCH", "DELETE"])
@login_required
def table_api(table_id):
    table = SchemaTable.query.get_or_404(table_id)
    if table.project.owner_id != session["user_id"]:
        return jsonify({"error": "Forbidden"}), 403
    if request.method == "DELETE":
        db.session.delete(table)
    else:
        payload = request.get_json(silent=True) or {}
        if "name" in payload:
            table.name = (payload["name"] or table.name).strip()[:128]
        table.position_x = payload.get("position_x", table.position_x)
        table.position_y = payload.get("position_y", table.position_y)
    db.session.commit()
    return jsonify({"ok": True})


@main.route("/api/schema/table/<int:table_id>/columns", methods=["POST"])
@login_required
def column_api(table_id):
    table = SchemaTable.query.get_or_404(table_id)
    if table.project.owner_id != session["user_id"]:
        return jsonify({"error": "Forbidden"}), 403
    payload = request.get_json(silent=True) or {}
    column = SchemaColumn(name=(payload.get("name") or "new_column").strip()[:128],
                          data_type=payload.get("data_type", "TEXT"),
                          is_nullable=payload.get("is_nullable", True), table_id=table.id)
    db.session.add(column)
    db.session.commit()
    return jsonify({"id": column.id, "name": column.name, "data_type": column.data_type}), 201