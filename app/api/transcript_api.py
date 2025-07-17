from flask import Blueprint, request, jsonify
from app.services.transcript_service import TranscriptService

bp = Blueprint('transcript_api', __name__)

@bp.route('/save_transcript', methods=['POST'])
def save_transcript():
    filename = request.form.get('filename')
    transcription = request.form.get('transcription')
    if not filename or not transcription:
        return jsonify({"error": "filename dan transcription wajib diisi"}), 400
    transcript = TranscriptService.save_transcript(filename, transcription)
    return jsonify({"message": "Transkrip berhasil disimpan", "id": transcript.id}), 200

@bp.route('/edit_transcript/<int:transcript_id>', methods=['PUT'])
def edit_transcript(transcript_id):
    filename = request.form.get('filename')
    transcription = request.form.get('transcription')
    transcript = TranscriptService.edit_transcript(transcript_id, filename, transcription)
    if not transcript:
        return jsonify({"error": "Transcript tidak ditemukan"}), 404
    return jsonify({"message": "Transkrip berhasil diupdate"}), 200

@bp.route('/delete_transcript/<int:transcript_id>', methods=['DELETE'])
def delete_transcript(transcript_id):
    success = TranscriptService.delete_transcript(transcript_id)
    if not success:
        return jsonify({"error": "Transcript tidak ditemukan"}), 404
    return jsonify({"message": "Transkrip berhasil dihapus"}), 200
