from flask import Blueprint, request, jsonify
from app.decorators.auth import jwt_required
from app.container import container

bp_stt = Blueprint('stt_api', __name__)

@bp_stt.route('/upload', methods=['POST'])
@jwt_required
def upload_audio(user_id: str):
    """
    Upload an audio file.
    Mengikuti SOLID principles dengan dependency injection dan single responsibility
    ---
    consumes:
      - multipart/form-data
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
        description: 'Bearer <JWT token>'
      - in: formData
        name: audio_file
        type: file
        required: true
        description: The audio file to upload (wav, m4a, etc)
    responses:
      200:
        description: Upload success
        schema:
          type: object
          properties:
            filename:
              type: string
      400:
        description: Bad request
    """
    if 'audio_file' not in request.files:
        return jsonify({"error": "No audio_file part in the request"}), 400
    
    file = request.files['audio_file']
    
    # Validasi file menggunakan service terpisah
    is_valid, error_message = container.file_validation_service.validate_file(file)
    if not is_valid:
        return jsonify({"error": error_message}), 400
    
    try:
        # Upload file menggunakan service terpisah
        unique_filename, _ = container.file_upload_service.save_file(file, user_id)
        return jsonify({"filename": unique_filename}), 200
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@bp_stt.route('/transcribe', methods=['POST'])
@jwt_required
def transcribe_audio(user_id: str):
    """
    Transcribe an uploaded audio file by filename.
    Mengikuti SOLID principles dengan dependency injection dan single responsibility
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
              description: The filename of uploaded audio file
    responses:
      200:
        description: Transcription result
        schema:
          type: object
          properties:
            transcription:
              type: string
      400:
        description: Bad request
      404:
        description: File not found
      500:
        description: Internal server error
    """
    data = request.get_json()
    filename = data.get('filename') if data else None
    if not filename:
        return jsonify({"error": "filename wajib diisi"}), 400
    
    # Cek apakah file ada menggunakan service terpisah
    if not container.file_upload_service.file_exists(user_id, filename):
        return jsonify({"error": "File tidak ditemukan"}), 404
    
    try:
        # Dapatkan path file dan lakukan transkripsi
        audio_path = container.file_upload_service.get_file_path(user_id, filename)
        transcribed_text = container.stt_service.transcribe(audio_path, language="id")
        
        
        return jsonify({"transcription": transcribed_text}), 200
    except Exception as e:
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500
    finally:
        # Hapus file setelah transkripsi selesai
        container.file_upload_service.delete_file(user_id, filename)
        
