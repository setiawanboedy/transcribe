from app.models.transcript import Transcript
from app.db.database import db

class TranscriptService:
    @staticmethod
    def save_transcript(filename, transcription, user_id):
        transcript = Transcript(filename=filename, transcription=transcription, user_id=user_id)
        db.session.add(transcript)
        db.session.commit()
        return transcript

    @staticmethod
    def edit_transcript(transcript_id, user_id, filename=None, transcription=None):
        transcript = Transcript.query.filter_by(id=transcript_id, user_id=user_id).first()
        if not transcript:
            return None
        if filename:
            transcript.filename = filename
        if transcription:
            transcript.transcription = transcription
        db.session.commit()
        return transcript

    @staticmethod
    def delete_transcript(transcript_id, user_id):
        transcript = Transcript.query.filter_by(id=transcript_id, user_id=user_id).first()
        if not transcript:
            return False
        db.session.delete(transcript)
        db.session.commit()
        return True

    @staticmethod
    def get_all_transcripts(user_id):
        return Transcript.query.filter_by(user_id=user_id).order_by(Transcript.created_at.desc()).all()
