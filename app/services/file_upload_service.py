import os
import uuid
from werkzeug.utils import secure_filename

class FileUploadService:
    """
    Service untuk menangani upload file
    Mengikuti Single Responsibility Principle - hanya bertanggung jawab untuk operasi file upload
    """
    
    def __init__(self, base_upload_dir: str = 'uploads'):
        self.base_upload_dir = base_upload_dir
    
    def generate_unique_filename(self, original_filename: str) -> str:
        """Generate nama file unik dengan UUID"""
        original_filename = secure_filename(original_filename)
        file_extension = os.path.splitext(original_filename)[1]
        return f"{uuid.uuid4().hex}{file_extension}"
    
    def get_user_upload_dir(self, user_id: str) -> str:
        """Dapatkan direktori upload untuk user tertentu"""
        return os.path.join(self.base_upload_dir, str(user_id))
    
    def ensure_upload_dir_exists(self, user_id: str) -> str:
        """Pastikan direktori upload user ada, buat jika belum ada"""
        user_dir = self.get_user_upload_dir(user_id)
        os.makedirs(user_dir, exist_ok=True)
        return user_dir
    
    def save_file(self, file, user_id: str) -> tuple[str, str]:
        """
        Simpan file ke direktori user
        Returns: (unique_filename, full_path)
        """
        unique_filename = self.generate_unique_filename(file.filename)
        user_dir = self.ensure_upload_dir_exists(user_id)
        full_path = os.path.join(user_dir, unique_filename)
        file.save(full_path)
        return unique_filename, full_path
    
    def get_file_path(self, user_id: str, filename: str) -> str:
        """Dapatkan path lengkap file user"""
        return os.path.join(self.get_user_upload_dir(user_id), secure_filename(filename))
    
    def file_exists(self, user_id: str, filename: str) -> bool:
        """Cek apakah file user ada"""
        file_path = self.get_file_path(user_id, filename)
        return os.path.exists(file_path)
    
    def delete_file(self, user_id: str, filename: str) -> bool:
        """
        Hapus file user
        Returns: True jika berhasil, False jika gagal
        """
        try:
            file_path = self.get_file_path(user_id, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False