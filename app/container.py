from typing import Protocol
from app.services.stt_service import STTService
from app.services.file_upload_service import FileUploadService
from app.services.file_validation_service import FileValidationService

class ISTTService(Protocol):
    """Interface untuk STT Service - Interface Segregation Principle"""
    def transcribe(self, audio_path: str, language: str = "id") -> str:
        ...

class IFileUploadService(Protocol):
    """Interface untuk File Upload Service"""
    def save_file(self, file, user_id: str) -> tuple[str, str]:
        ...
    
    def get_file_path(self, user_id: str, filename: str) -> str:
        ...
    
    def file_exists(self, user_id: str, filename: str) -> bool:
        ...
        
    def delete_file(self, user_id: str, filename: str) -> bool:
        ...

class IFileValidationService(Protocol):
    """Interface untuk File Validation Service"""
    @staticmethod
    def validate_file(file) -> tuple[bool, str]:
        ...

class ServiceContainer:
    """
    Dependency Injection Container
    Mengikuti Dependency Inversion Principle - depend on abstractions, not concretions
    """
    
    def __init__(self):
        self._stt_service = None
        self._file_upload_service = None
        self._file_validation_service = None
    
    @property
    def stt_service(self) -> ISTTService:
        if self._stt_service is None:
            self._stt_service = STTService()
        return self._stt_service
    
    @property
    def file_upload_service(self) -> IFileUploadService:
        if self._file_upload_service is None:
            self._file_upload_service = FileUploadService()
        return self._file_upload_service
    
    @property
    def file_validation_service(self) -> IFileValidationService:
        if self._file_validation_service is None:
            self._file_validation_service = FileValidationService()
        return self._file_validation_service

# Global container instance
container = ServiceContainer()