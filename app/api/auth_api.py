from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

bp_auth = Blueprint('auth_api', __name__)

@bp_auth.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: User registered
      400:
        description: Bad request
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "username dan password wajib diisi"}), 400
    user = AuthService.register(username, password)
    if not user:
        return jsonify({"error": "Username sudah terdaftar"}), 400
    return jsonify({"message": "User registered"}), 200

@bp_auth.route('/login', methods=['POST'])
def login():
    """
    Login user.
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login success
      401:
        description: Unauthorized
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = AuthService.authenticate(username, password)
    if not user:
        return jsonify({"error": "Username atau password salah"}), 401
    return jsonify({"message": "Login success", "user_id": user.id}), 200
