from werkzeug.utils import secure_filename
from typing import Optional, Tuple

class FileValidationService:
    """
    Service untuk validasi file
    Mengikuti Single Responsibility Principle - hanya bertanggung jawab untuk validasi file
    """
    
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'flac', 'ogg', 'aac'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    @staticmethod
    def is_allowed_file(filename: str) -> bool:
        """Cek apakah ekstensi file diizinkan"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in FileValidationService.ALLOWED_EXTENSIONS
    
    @staticmethod
    def validate_file(file) -> Tuple[bool, Optional[str]]:
        """
        Validasi file yang di-upload
        Returns: (is_valid, error_message)
        """
        if not file:
            return False, "No file provided"
        
        if file.filename == '':
            return False, "No selected file"
        
        if not FileValidationService.is_allowed_file(file.filename):
            return False, f"File type not allowed. Allowed: {', '.join(FileValidationService.ALLOWED_EXTENSIONS)}"
        
        # Check file size if possible
        file.seek(0, 2)  # Seek to end
        size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if size > FileValidationService.MAX_FILE_SIZE:
            return False, f"File too large. Maximum size: {FileValidationService.MAX_FILE_SIZE // (1024*1024)}MB"
        
        return True, None