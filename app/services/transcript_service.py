from app.models.transcript import Transcript
from app.db.database import db

class TranscriptService:
    @staticmethod
    def save_transcript(filename, transcription):
        transcript = Transcript(filename=filename, transcription=transcription)
        db.session.add(transcript)
        db.session.commit()
        return transcript

    @staticmethod
    def edit_transcript(transcript_id, filename=None, transcription=None):
        transcript = Transcript.query.get(transcript_id)
        if not transcript:
            return None
        if filename:
            transcript.filename = filename
        if transcription:
            transcript.transcription = transcription
        db.session.commit()
        return transcript

    @staticmethod
    def delete_transcript(transcript_id):
        transcript = Transcript.query.get(transcript_id)
        if not transcript:
            return False
        db.session.delete(transcript)
        db.session.commit()
        return True
