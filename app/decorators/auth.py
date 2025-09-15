from functools import wraps
from flask import request, jsonify
from app.services.jwt_service import JWTService

def jwt_required(f):
    """
    Decorator untuk validasi JWT token
    Mengikuti Single Responsibility Principle - hanya bertanggung jawab untuk autentikasi
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization token required"}), 401
        
        parts = auth_header.split(' ', 1)
        token = parts[1].strip() if len(parts) > 1 else ''
        if not token:
            return jsonify({"error": "Authorization token required"}), 401
        
        token_data = JWTService.decode_token(token)
        if not token_data:
            return jsonify({"error": "Token tidak valid atau expired"}), 401
        
        user_id = token_data["user_id"]
        if not user_id:
            return jsonify({"error": "Token tidak valid atau expired"}), 401
        
        # Inject user_id ke function
        return f(user_id, *args, **kwargs)
    
    return decorated_function