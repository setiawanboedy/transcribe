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
        print(f"[JWT DEBUG] ENCODE: SECRET_KEY={SECRET_KEY}, PAYLOAD={payload}, TOKEN={token}")
        return token

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            print(f"[JWT DEBUG] DECODE: SECRET_KEY={SECRET_KEY}, TOKEN={token}, PAYLOAD={payload}")
            return payload['sub']
        except jwt.ExpiredSignatureError:
            print(f"[JWT DEBUG] DECODE ERROR: ExpiredSignatureError, SECRET_KEY={SECRET_KEY}, TOKEN={token}")
            return None
        except jwt.InvalidTokenError:
            print(f"[JWT DEBUG] DECODE ERROR: InvalidTokenError, SECRET_KEY={SECRET_KEY}, TOKEN={token}")
            return None
