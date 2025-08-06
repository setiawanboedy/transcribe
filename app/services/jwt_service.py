import os
import jwt
import datetime
from flask import current_app

SECRET_KEY = os.environ.get("SECRET_KEY", "transcript-secret-key")  # Ganti dengan env var di production

class JWTService:
    @staticmethod
    def encode_token(user_id):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': str(user_id)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return token

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return {
                "user_id": payload['sub'],
                "expired_at": payload['exp']
            }
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
