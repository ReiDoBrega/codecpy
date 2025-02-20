from typing import List, Optional
from dataclasses import dataclass
from enum import Enum, auto

from codecpy.colors import ColorInfo
from codecpy.profiles import ProfileInfo


class CodecType(Enum):
    """Enum representing the different types of codecs"""
    AUDIO = auto()
    VIDEO = auto()
    TEXT = auto()
    IMAGE = auto()
    UNKNOWN = auto()
    
    @classmethod
    def from_string(cls, type_str: str) -> 'CodecType':
        """Convert string representation to CodecType enum"""
        type_map = {
            'audio': cls.AUDIO,
            'video': cls.VIDEO,
            'text': cls.TEXT,
            'image': cls.IMAGE,
            'unknown': cls.UNKNOWN
        }
        return type_map.get(type_str.lower(), cls.UNKNOWN)
    
    def to_string(self) -> str:
        """Convert CodecType enum to string representation"""
        return self.name.lower()

@dataclass
class CodecInfo:
    """Class representing normalized codec information"""
    original: str
    normalized: str
    type: CodecType
    technical_id: str
    family: Optional[str] = None
    
    @classmethod
    def create_unknown(cls, original: Optional[str] = None) -> 'CodecInfo':
        """Create an unknown codec information object"""
        return cls(
            original=original,
            normalized='UNKNOWN',
            type=CodecType.UNKNOWN,
            technical_id=None,
            family=None
        )

@dataclass
class CodecDetails:
    """Class representing comprehensive codec details"""
    original: str
    normalized: str
    type: CodecType
    family: Optional[str]
    profiles: Optional[ProfileInfo] = None
    color_info: Optional[ColorInfo] = None

@dataclass
class CodecStreamInfo:
    """Class representing details about a media stream with multiple codecs"""
    original: str
    codecs: List[CodecInfo]
    has_video: bool = False
    has_audio: bool = False
    has_text: bool = False
    video_codec: Optional[str] = None
    audio_codec: Optional[str] = None


@dataclass
class AudioCodecDetails(CodecDetails):
    """Class representing comprehensive audio codec details"""
    channels: Optional[str] = None
    sample_rate: Optional[int] = None
    bit_depth: Optional[int] = None
