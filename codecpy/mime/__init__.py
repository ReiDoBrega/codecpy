from typing import Dict, List
from codecpy.mime.info import MimeTypeInfo


class MimeTypeUtil:
    """Utility class for MIME type handling"""
    
    # Common MIME type mappings
    _COMMON_MIME_TYPES: Dict[str, str] = {
        # Video formats
        "mp4": "video/mp4",
        "webm": "video/webm",
        "ogg": "video/ogg",
        "avi": "video/x-msvideo",
        "mov": "video/quicktime",
        "mkv": "video/x-matroska",
        "flv": "video/x-flv",
        
        # Audio formats
        "mp3": "audio/mpeg",
        "wav": "audio/wav",
        "aac": "audio/aac",
        "flac": "audio/flac",
        "m4a": "audio/mp4",
        "opus": "audio/opus",
        
        # Image formats
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
        "svg": "image/svg+xml",
        
        # Text formats
        "txt": "text/plain",
        "html": "text/html",
        "css": "text/css",
        "js": "text/javascript",
        "json": "application/json",
        "xml": "application/xml",
        
        # Application formats
        "pdf": "application/pdf",
        "zip": "application/zip",
        "doc": "application/msword",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }
    
    # MIME type to CodecType mapping
    _MIME_TYPE_TO_CODEC_TYPE: Dict[str, str] = {
        "video": "video",
        "audio": "audio",
        "image": "image",
        "text": "text",
        "application": "unknown"
    }
    
    @classmethod
    def parse_mime_type(cls, mime_type_str: str) -> MimeTypeInfo:
        """
        Parse a MIME type string into its components
        
        Args:
            mime_type_str: MIME type string (e.g. 'video/mp4; codecs="avc1.640028, mp4a.40.2"')
            
        Returns:
            MimeTypeInfo object with parsed components
        """
        if not mime_type_str:
            return MimeTypeInfo(
                full_type="application/octet-stream",
                main_type="application",
                sub_type="octet-stream",
                parameters={}
            )
            
        # Split type and parameters
        parts = mime_type_str.split(';')
        type_part = parts[0].strip()
        
        # Parse main type and subtype
        type_components = type_part.split('/')
        if len(type_components) != 2:
            main_type, sub_type = "application", "octet-stream"
        else:
            main_type, sub_type = type_components
            
        # Parse parameters
        parameters = {}
        for param in parts[1:]:
            param = param.strip()
            if '=' in param:
                key, value = param.split('=', 1)
                parameters[key.strip()] = value.strip()
        
        return MimeTypeInfo(
            full_type=type_part,
            main_type=main_type,
            sub_type=sub_type,
            parameters=parameters
        )
    
    @classmethod
    def get_mime_type_for_extension(cls, extension: str) -> str:
        """
        Get MIME type string for a file extension
        
        Args:
            extension: File extension (e.g. 'mp4', 'mp3')
            
        Returns:
            MIME type string
        """
        ext = extension.lower().lstrip('.')
        return cls._COMMON_MIME_TYPES.get(ext, "application/octet-stream")
    
    @classmethod
    def get_extension_for_mime_type(cls, mime_type: str) -> List[str]:
        """
        Get possible file extensions for a MIME type
        
        Args:
            mime_type: MIME type string (e.g. 'video/mp4')
            
        Returns:
            List of possible file extensions
        """
        mime_type = mime_type.split(';')[0].strip().lower()
        extensions = []
        
        for ext, mime in cls._COMMON_MIME_TYPES.items():
            if mime.lower() == mime_type:
                extensions.append(ext)
                
        return extensions
    
    @classmethod
    def create_mime_type_with_codecs(cls, mime_base: str, codecs: List[str]) -> str:
        """
        Create a MIME type string with codecs parameter
        
        Args:
            mime_base: Base MIME type (e.g. 'video/mp4')
            codecs: List of codec strings
            
        Returns:
            MIME type string with codecs parameter
        """
        if not codecs:
            return mime_base
            
        codec_str = ", ".join(codecs)
        return f'{mime_base}; codecs="{codec_str}"'
    
    @classmethod
    def get_codec_type_from_mime(cls, mime_type: str) -> str:
        """
        Get the codec type based on MIME type
        
        Args:
            mime_type: MIME type string
            
        Returns:
            String representing codec type ('video', 'audio', 'text', 'image', 'unknown')
        """
        mime_info = cls.parse_mime_type(mime_type)
        return cls._MIME_TYPE_TO_CODEC_TYPE.get(mime_info.main_type, "unknown")
    