from app.models.user import User
from app.db.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    @staticmethod
    def register(username, password):
        if User.query.filter_by(username=username).first():
            return None  # User already exists
        hashed = generate_password_hash(password)
        user = User(username=username, password=hashed)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return user
        return None
