import os
from faster_whisper import WhisperModel

class STTService:
    _model = None
    _model_path = os.environ.get("MODEL_PATH", "./models/faster-whisper-medium-id")
    _device = os.environ.get("DEVICE", "cpu")
    _compute_type = os.environ.get("COMPUTE_TYPE", "int8")

    @classmethod
    def get_model(cls):
        if cls._model is None:
            if not os.path.exists(cls._model_path):
                raise FileNotFoundError(f"Direktori model tidak ditemukan: {cls._model_path}. Pastikan model diunduh.")
            print(f"Memuat model Whisper dari {cls._model_path} pada perangkat {cls._device} dengan compute_type={cls._compute_type}")
            cls._model = WhisperModel(cls._model_path, device=cls._device, compute_type=cls._compute_type)
            print("Model berhasil dimuat.")
        return cls._model

    @classmethod
    def transcribe(cls, audio_path, language="id"):
        model = cls.get_model()
        print(f"Mentranskripsi file audio: {audio_path} (Bahasa: {language})...")
        segments, info = model.transcribe(audio_path, language=language, beam_size=5)
        full_transcription = []
        for segment in segments:
            full_transcription.append(segment.text)
        print("Transkripsi selesai.")
        return " ".join(full_transcription)
