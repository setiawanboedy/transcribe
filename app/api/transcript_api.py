from flask import Blueprint, request, jsonify
from app.services.transcript_service import TranscriptService

bp = Blueprint('transcript_api', __name__)


@bp.route('/all_transcripts', methods=['GET'])
def get_all_transcripts():
    """
    Ambil semua hasil transkrip yang tersimpan di database.
    ---
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
        description: 'Bearer <JWT token>'
    responses:
      200:
        description: Daftar semua transkrip
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              filename:
                type: string
              transcription:
                type: string
              created_at:
                type: string
    """
    from app.services.jwt_service import JWTService
    auth_header = request.headers.get('Authorization')
    print(f"[TRANSCRIPT DEBUG] Authorization header: {auth_header}")
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization token required"}), 401
    parts = auth_header.split(' ', 1)
    token = parts[1].strip() if len(parts) > 1 else ''
    print(f"[TRANSCRIPT DEBUG] Token parsed: {token}")
    if not token:
        return jsonify({"error": "Authorization token required"}), 401
    user_id = JWTService.decode_token(token)
    print(f"[TRANSCRIPT DEBUG] user_id from token: {user_id}")
    if not user_id:
        return jsonify({"error": "Token tidak valid atau expired"}), 401
    transcripts = TranscriptService.get_all_transcripts(user_id)
    result = []
    for t in transcripts:
        result.append({
            "id": t.id,
            "filename": t.filename,
            "transcription": t.transcription,
            "created_at": t.created_at.isoformat() if t.created_at else None
        })
    return jsonify(result), 200

@bp.route('/save_transcript', methods=['POST'])
def save_transcript():
    """
    Simpan hasil transkripsi ke database SQLite.
    ---
    consumes:
      - application/json
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
        description: 'Bearer <JWT token>'
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            filename:
              type: string
            transcription:
              type: string
    responses:
      200:
        description: Transkrip berhasil disimpan
        schema:
          type: object
          properties:
            message:
              type: string
            id:
              type: integer
      400:
        description: Bad request
    """
    from app.services.jwt_service import JWTService
    auth_header = request.headers.get('Authorization')
    print(f"[TRANSCRIPT DEBUG] Authorization header: {auth_header}")
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization token required"}), 401
    parts = auth_header.split(' ', 1)
    token = parts[1].strip() if len(parts) > 1 else ''
    print(f"[TRANSCRIPT DEBUG] Token parsed: {token}")
    if not token:
        return jsonify({"error": "Authorization token required"}), 401
    user_id = JWTService.decode_token(token)
    print(f"[TRANSCRIPT DEBUG] user_id from token: {user_id}")
    if not user_id:
        return jsonify({"error": "Token tidak valid atau expired"}), 401
    data = request.get_json()
    filename = data.get('filename') if data else None
    transcription = data.get('transcription') if data else None
    if not filename or not transcription:
        return jsonify({"error": "filename dan transcription wajib diisi"}), 400
    transcript = TranscriptService.save_transcript(filename, transcription, user_id)
    return jsonify({"message": "Transkrip berhasil disimpan", "id": transcript.id}), 200

@bp.route('/edit_transcript/<int:transcript_id>', methods=['PUT'])
def edit_transcript(transcript_id):
    """
    Edit transcript yang sudah disimpan di database.
    ---
    consumes:
      - application/json
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
        description: 'Bearer <JWT token>'
      - in: path
        name: transcript_id
        type: integer
        required: true
        description: ID transcript yang akan diedit
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            filename:
              type: string
            transcription:
              type: string
    responses:
      200:
        description: Transkrip berhasil diupdate
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Transcript tidak ditemukan
    """
    from app.services.jwt_service import JWTService
    auth_header = request.headers.get('Authorization')
    print(f"[TRANSCRIPT DEBUG] Authorization header: {auth_header}")
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization token required"}), 401
    parts = auth_header.split(' ', 1)
    token = parts[1].strip() if len(parts) > 1 else ''
    print(f"[TRANSCRIPT DEBUG] Token parsed: {token}")
    if not token:
        return jsonify({"error": "Authorization token required"}), 401
    user_id = JWTService.decode_token(token)
    print(f"[TRANSCRIPT DEBUG] user_id from token: {user_id}")
    if not user_id:
        return jsonify({"error": "Token tidak valid atau expired"}), 401
    data = request.get_json()
    filename = data.get('filename') if data else None
    transcription = data.get('transcription') if data else None
    transcript = TranscriptService.edit_transcript(transcript_id, user_id, filename, transcription)
    if not transcript:
        return jsonify({"error": "Transcript tidak ditemukan"}), 404
    return jsonify({"message": "Transkrip berhasil diupdate"}), 200

@bp.route('/delete_transcript/<int:transcript_id>', methods=['DELETE'])
def delete_transcript(transcript_id):
    """
    Hapus transcript dari database.
    ---
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
        description: 'Bearer <JWT token>'
      - in: path
        name: transcript_id
        type: integer
        required: true
        description: ID transcript yang akan dihapus
    responses:
      200:
        description: Transkrip berhasil dihapus
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Transcript tidak ditemukan
    """
    from app.services.jwt_service import JWTService
    auth_header = request.headers.get('Authorization')
    print(f"[TRANSCRIPT DEBUG] Authorization header: {auth_header}")
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization token required"}), 401
    parts = auth_header.split(' ', 1)
    token = parts[1].strip() if len(parts) > 1 else ''
    print(f"[TRANSCRIPT DEBUG] Token parsed: {token}")
    if not token:
        return jsonify({"error": "Authorization token required"}), 401
    user_id = JWTService.decode_token(token)
    print(f"[TRANSCRIPT DEBUG] user_id from token: {user_id}")
    if not user_id:
        return jsonify({"error": "Token tidak valid atau expired"}), 401
    success = TranscriptService.delete_transcript(transcript_id, user_id)
    if not success:
        return jsonify({"error": "Transcript tidak ditemukan"}), 404
    return jsonify({"message": "Transkrip berhasil dihapus"}), 200
