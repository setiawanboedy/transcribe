from dotenv import load_dotenv # type: ignore
load_dotenv() 
from flask import Flask, request, jsonify # type: ignore
from faster_whisper import WhisperModel # type: ignore
from werkzeug.utils import secure_filename # type: ignore
import tempfile

import os
from dotenv import load_dotenv # type: ignore
load_dotenv()
from flask import Flask, request, jsonify # type: ignore
from faster_whisper import WhisperModel # type: ignore
from werkzeug.utils import secure_filename # type: ignore
import tempfile
# Flasgger for Swagger UI
from flasgger import Swagger
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# ---------------------------------------------------------------------------
# Konfigurasi
# Menggunakan variabel untuk konfigurasi yang lebih baik di server
# MODEL_PATH = os.environ.get("MODEL_PATH", "./models/faster-whisper-medium-id") # alamat model stt
MODEL_PATH = os.environ.get("MODEL_PATH", "./models/faster-whisper-medium-id") # alamat model stt
# Ganti "cpu" dengan "cuda" jika GPU tersedia untuk performa yang lebih baik.
# Gunakan compute_type="float16" atau "int8_float16" untuk GPU, dan "int8" untuk CPU.
DEVICE = os.environ.get("DEVICE", "cpu")
COMPUTE_TYPE = os.environ.get("COMPUTE_TYPE", "int8")

app = Flask(__name__)
# Inisialisasi Swagger dengan route yang pasti
swagger = Swagger(app, config={
    'headers': [],
    'specs': [
        {
            'endpoint': 'apispec_1',
            'route': '/apispec_1.json',
            'rule_filter': lambda rule: True,  # all in
            'model_filter': lambda tag: True,  # all in
        }
    ],
    'static_url_path': '/flasgger_static',
    'swagger_ui': True,
    'specs_route': '/apidocs/'
})

# Optional: root endpoint for health check
@app.route('/')
def index():
    return 'API is running. Swagger UI: <a href="/apidocs/">/apidocs/</a>'

# Memuat model STT secara global saat aplikasi dimulai
# Ini memastikan model hanya dimuat sekali
stt_model = None

def load_stt_model(local_model_path, device, compute_type):
    """
    Memuat model Whisper dari direktori lokal.
    Args:
        local_model_path (str): alamat ke direktori yang berisi file model stt.
        device (str): Perangkat untuk inferensi (misalnya, "cpu", "cuda").
        compute_type (str): Tipe komputasi untuk inferensi (misalnya, "float32", "float16", "int8", "int8_float16").
                            "int8" sering direkomendasikan untuk CPU.
                            "float16" atau "int8_float16" direkomendasikan untuk GPU.
    Returns:
        WhisperModel: model faster-whisper yang dimuat.
    """
    if not os.path.exists(local_model_path):
        raise FileNotFoundError(f"Direktori model tidak ditemukan: {local_model_path}. Pastikan model diunduh menggunakan HuggingFace snapshot_download.")

    print(f"Memuat model Whisper dari {local_model_path} pada perangkat {device} dengan compute_type={compute_type}")
    model = WhisperModel(local_model_path, device=device, compute_type=compute_type)
    print("Model berhasil dimuat.")
    return model

def transcribe_audio_file(model, audio_path, language="id"):
    """
    Mentranskripsi file audio menggunakan model stt yang dimuat.
    Args:
        model (WhisperModel): model faster-whisper yang dimuat.
        audio_path (str): alamat ke file audio.
        language (str): Bahasa audio (misalnya, "en" untuk Inggris, "id" untuk Indonesia).
    Returns:
        str: Transkripsi lengkap dari file audio.
    """
    print(f"Mentranskripsi file audio: {audio_path} (Bahasa: {language})...")
    # Parameter lain yang dapat disesuaikan untuk optimasi lebih lanjut:
    # beam_size: Meningkatkan akurasi tetapi memperlambat proses (default: 5)
    # hotwords: Kata-kata kunci untuk meningkatkan akurasi transkripsi
    # initial_prompt: Memberikan konteks awal kepada model
    segments, info = model.transcribe(audio_path, language=language, beam_size=5)

    full_transcription = []
    #print(f"Deteksi bahasa: {info.language} dengan probabilitas {info.language_probability:.4f}")

    for segment in segments:
        full_transcription.append(segment.text)
        # print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

    print("Transkripsi selesai.")
    return " ".join(full_transcription)

@app.before_request
def initialize_model():
    """
    Memuat model STT jika belum dimuat.
    Ini dipanggil sekali saat aplikasi dimulai, sebelum permintaan pertama.
    """
    global stt_model
    if stt_model is None:
        try:
            stt_model = load_stt_model(MODEL_PATH, DEVICE, COMPUTE_TYPE)
        except Exception as e:
            print(f"Error loading model: {e}")
            # Tangani error pemuatan model, mungkin keluar atau mengembalikan error
            exit(1) # Keluar jika model tidak dapat dimuat

@app.route('/transcribe', methods=['POST'])
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

    if file:
        filename = secure_filename(file.filename)
        # Menggunakan file sementara untuk menyimpan audio yang diunggah
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_audio_file:
            file.save(temp_audio_file.name)
            temp_audio_path = temp_audio_file.name

        try:
            transcribed_text = transcribe_audio_file(stt_model, temp_audio_path, language="id")
            return jsonify({"transcription": transcribed_text}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            # Pastikan file sementara dihapus
            os.unlink(temp_audio_path)

if __name__ == '__main__':
    # Untuk menjalankan aplikasi Flask
    app.run(host='0.0.0.0', port=5000, debug=False) # Set debug=True hanya untuk pengembangan