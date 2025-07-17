from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import tempfile
import os
from app.services.stt_service import STTService

bp_stt = Blueprint('stt_api', __name__)

@bp_stt.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Transcribe an uploaded audio file.
    ---
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: audio_file
        type: file
        required: true
        description: The audio file to transcribe (wav, m4a, etc)
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
      500:
        description: Internal server error
    """
    if 'audio_file' not in request.files:
        return jsonify({"error": "No audio_file part in the request"}), 400
    file = request.files['audio_file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    filename = secure_filename(file.filename)
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_audio_file:
        file.save(temp_audio_file.name)
        temp_audio_path = temp_audio_file.name
    try:
        transcribed_text = STTService.transcribe(temp_audio_path, language="id")
        return jsonify({"transcription": transcribed_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.unlink(temp_audio_path)
