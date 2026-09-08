from datetime import datetime, timedelta, timezone
from io import BytesIO
import secrets

from functools import wraps

from flask import Blueprint, current_app, jsonify, request, send_file, session
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db
from .models import AuthSession, Item, LessonProgress, LoginAttempt, User

api_bp = Blueprint("api", __name__)
auth_bp = Blueprint("auth", __name__)
ALLOWED_THEMES = {"paper", "dark", "red", "blue", "mono"}
MAX_PROFILE_PICTURE_BYTES = 2 * 1024 * 1024


def require_user(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = current_user()
        if not user:
            return jsonify({"error": "authentication required"}), 401
        return view(user, *args, **kwargs)

    return wrapped


def current_user():
    user_id = session.get("user_id")
    session_id = session.get("session_id")
    if not user_id or not session_id:
        return None

    auth_session = AuthSession.query.filter_by(session_id=session_id, user_id=user_id, revoked_at=None).first()
    expires_at = auth_session.expires_at if auth_session else None
    if expires_at and expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if not auth_session or expires_at < datetime.now(timezone.utc):
        session.clear()
        return None

    auth_session.last_seen_at = datetime.now(timezone.utc)
    db.session.commit()
    return db.session.get(User, user_id)


def client_ip():
    return request.remote_addr or "unknown"


def login_attempts_exceeded(email):
    window_start = datetime.now(timezone.utc) - timedelta(seconds=current_app.config["AUTH_LOGIN_WINDOW_SECONDS"])
    return LoginAttempt.query.filter(
        LoginAttempt.email == email,
        LoginAttempt.ip_address == client_ip(),
        LoginAttempt.attempted_at >= window_start,
    ).count() >= current_app.config["AUTH_LOGIN_LIMIT"]


def record_login_attempt(email):
    db.session.add(LoginAttempt(email=email, ip_address=client_ip()))
    db.session.commit()


def start_session(user):
    now = datetime.now(timezone.utc)
    auth_session = AuthSession(
        session_id=secrets.token_urlsafe(32),
        user_id=user.id,
        created_at=now,
        last_seen_at=now,
        expires_at=now + timedelta(seconds=current_app.config["AUTH_SESSION_LIFETIME_SECONDS"]),
        ip_address=client_ip(),
        user_agent=request.headers.get("User-Agent", "")[:500],
    )
    db.session.add(auth_session)
    db.session.commit()
    session.clear()
    session["user_id"] = user.id
    session["session_id"] = auth_session.session_id


def profile_user(user):
    return jsonify({"user": user.to_dict()})


@api_bp.get("/health")
def health_check():
    return jsonify({"status": "ok", "service": "blocky-api"})


@auth_bp.post("/signup")
def signup():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name", "").strip()
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "")

    if not name or not email or not password:
        return jsonify({"error": "name, email, and password are required"}), 400
    if len(password) < 8:
        return jsonify({"error": "password must be at least 8 characters"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "an account with that email already exists"}), 409

    user = User(name=name, email=email, password_hash=generate_password_hash(password))
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "an account with that email already exists"}), 409

    start_session(user)
    return jsonify({"user": user.to_dict()}), 201


@auth_bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "")
    if login_attempts_exceeded(email):
        return jsonify({"error": "too many failed login attempts; try again later"}), 429

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        record_login_attempt(email)
        return jsonify({"error": "invalid email or password"}), 401

    start_session(user)
    return jsonify({"user": user.to_dict()})


@auth_bp.post("/logout")
def logout():
    session_id = session.get("session_id")
    if session_id:
        auth_session = AuthSession.query.filter_by(session_id=session_id).first()
        if auth_session:
            auth_session.revoked_at = datetime.now(timezone.utc)
            db.session.commit()
    session.clear()
    return jsonify({"message": "logged out"})


@auth_bp.get("/sessions")
def sessions():
    user = current_user()
    if not user:
        return jsonify({"error": "authentication required"}), 401

    active_sessions = AuthSession.query.filter(
        AuthSession.user_id == user.id,
        AuthSession.revoked_at.is_(None),
        AuthSession.expires_at > datetime.now(timezone.utc),
    ).order_by(AuthSession.last_seen_at.desc()).all()
    current_session_id = session.get("session_id")
    return jsonify({
        "sessions": [
            {
                "id": item.id,
                "current": item.session_id == current_session_id,
                "created_at": item.created_at.isoformat(),
                "last_seen_at": item.last_seen_at.isoformat(),
                "expires_at": item.expires_at.isoformat(),
                "ip_address": item.ip_address,
                "user_agent": item.user_agent,
            }
            for item in active_sessions
        ]
    })


@auth_bp.get("/me")
def me():
    user = current_user()
    if not user:
        return jsonify({"user": None}), 200
    return jsonify({"user": user.to_dict()})


@auth_bp.patch("/profile")
@require_user
def update_profile(user):
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    theme = payload.get("theme")

    if name is not None:
        name = name.strip()
        if not name:
            return jsonify({"error": "name cannot be empty"}), 400
        user.name = name
    if theme is not None:
        if theme not in ALLOWED_THEMES:
            return jsonify({"error": "unsupported theme"}), 400
        user.theme = theme

    db.session.commit()
    return profile_user(user)


@auth_bp.post("/profile/avatar")
@require_user
def upload_avatar(user):
    picture = request.files.get("picture")
    if not picture or not picture.mimetype.startswith("image/"):
        return jsonify({"error": "upload an image file"}), 400

    picture_bytes = picture.read(MAX_PROFILE_PICTURE_BYTES + 1)
    if len(picture_bytes) > MAX_PROFILE_PICTURE_BYTES:
        return jsonify({"error": "profile pictures must be 2 MB or smaller"}), 413

    user.profile_picture = picture_bytes
    user.profile_picture_type = picture.mimetype
    db.session.commit()
    return profile_user(user)


@auth_bp.get("/avatar/<int:user_id>")
def avatar(user_id):
    user = db.session.get(User, user_id)
    if not user or not user.profile_picture:
        return jsonify({"error": "profile picture not found"}), 404
    return send_file(
        BytesIO(user.profile_picture),
        mimetype=user.profile_picture_type or "image/jpeg",
    )


@auth_bp.post("/lessons/<lesson_id>/complete")
@require_user
def complete_lesson(user, lesson_id):
    existing = LessonProgress.query.filter_by(user_id=user.id, lesson_id=lesson_id).first()
    if existing:
        return jsonify({"completed": True, "awarded": 0, "points": user.points, "lessons_completed": len(user.lesson_progress)})

    db.session.add(LessonProgress(user_id=user.id, lesson_id=lesson_id))
    user.points += 1
    db.session.commit()
    return jsonify({"completed": True, "awarded": 1, "points": user.points, "lessons_completed": len(user.lesson_progress)}), 201


@auth_bp.get("/progress")
@require_user
def progress(user):
    return jsonify({
        "points": user.points,
        "lessons_completed": [item.lesson_id for item in user.lesson_progress],
    })


@api_bp.get("/items")
def list_items():
    items = Item.query.order_by(Item.created_at.desc()).all()
    return jsonify([item.to_dict() for item in items])


@api_bp.post("/items")
def create_item():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name", "").strip()
    description = payload.get("description", "").strip()

    if not name:
        return jsonify({"error": "name is required"}), 400

    item = Item(name=name, description=description)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201
