import re
from typing import Dict, Optional, List, Tuple, Union

from loggpy import Logger

from codecpy.codecs import AudioCodecDetails, CodecDetails, CodecInfo, CodecStreamInfo, CodecType
from codecpy.colors import ColorInfo
from codecpy.profiles import ProfileInfo
from codecpy.container import ContainerInfo
from codecpy.mime import MimeTypeUtil


class CodecPy:
    """
    A professional library for processing and normalizing codec strings to human-readable formats.
    Handles a wide range of audio and video codecs with comprehensive mapping and pattern recognition.
    """
    
    # Audio codec mappings - extensive with all variants
    _AUDIO_CODEC_MAP: Dict[str, str] = {
        # PCM variants
        "1": "PCM",
        "pcm": "PCM",
        
        # AAC variants
        "aacl": "AAC",
        "aac": "AAC",
        "mp4a.66": "AAC_MPEG2",
        "mp4a.67": "AAC_MPEG2",
        "mp4a.68": "AAC_MPEG2",
        "mp4a.40.2": "AAC_LC",
        "mp4a.40.02": "AAC_LC",
        "mp4a.40.5": "AAC_HE",
        "mp4a.40.05": "AAC_HE",
        "mp4a.40.29": "AAC_HE_V2",
        "mp4a.40.42": "AAC_XHE",
        
        # MP3 variants
        "mp3": "MP3",
        "mp4a.69": "MP3",
        "mp4a.6b": "MP3",
        "mp4a.6B": "MP3",
        
        # Dolby variants
        "ac-3": "AC3",
        "mp4a.a5": "AC3",
        "mp4a.A5": "AC3",
        "ec-3": "EAC3",
        "e-ac3": "EAC3",
        "ec3": "EAC3",
        "mp4a.a6": "EAC3",
        "mp4a.A6": "EAC3",
        "ac-4": "AC4",
        
        # DTS variants
        "dts": "DTS",
        "dts-hd": "DTS_HD",
        "dts-hdma": "DTS_HD_MA",
        "dts-hdhr": "DTS_HD_HRA",
        "dts-x": "DTS_X",
        "dtse": "DTS_EXPRESS",
        "dtsl": "DTS_LOSSLESS",
        "mp4a.a9": "DTS",
        "mp4a.A9": "DTS",
        "mp4a.ac": "DTS_HD",
        "mp4a.AC": "DTS_HD",
        
        # Other audio codecs
        "vorbis": "VORBIS",
        "opus": "OPUS",
        "flac": "FLAC",
        "alac": "ALAC",
        "speex": "SPEEX",
        "mp2": "MP2",
        "mp2a": "MP2",
        "amr": "AMR",
        "amr-wb": "AMR_WB",
        "pcma": "G711_A_LAW",
        "pcmu": "G711_MU_LAW",
    }
    
    # Video codec mappings
    _VIDEO_CODEC_MAP: Dict[str, str] = {
        # H.264 variants
        "avc": "H264",
        "avc1": "H264",
        "avc3": "H264",
        
        # H.265/HEVC variants
        "hev1": "H265",
        "hvc1": "H265",
        "hevc": "H265",
        
        # Dolby Vision
        "dvh1": "DOVI",
        "dvhe": "DOVI",
        
        # VP variants
        "vp8": "VP8",
        "vp8.0": "VP8",
        "vp09": "VP9",
        "vp9": "VP9",
        "vp9.0": "VP9",
        "vp9.1": "VP9", 
        "vp9.2": "VP9",
        "vp9.3": "VP9",
        "av01": "AV1",
        
        # Other video codecs
        "theora": "THEORA",
        "h263": "H263",
        "mpeg2": "MPEG2",
        "mp4v": "MPEG4",
        "mp4v.20.9": "MPEG4",
        "rv40": "REAL_VIDEO",
    }
    
    # Text/Subtitle codec mappings
    _TEXT_CODEC_MAP: Dict[str, str] = {
        "wvtt": "WEBVTT",
        "ttml": "TTML",
        "stpp": "TTML_MP4",
        "cea608": "CEA_608",
        "cea708": "CEA_708",
        "subt": "SUBTITLE",
        "sbtt": "SUBTITLE",
        "tx3g": "TEXT_TX3G",
        "text": "TEXT_PLAIN",
        "srt": "SRT",
        "ssa": "SSA",
        "ass": "ASS",
    }
    
    # Image codec mappings
    _IMAGE_CODEC_MAP: Dict[str, str] = {
        "jpeg": "JPEG",
        "png": "PNG",
        "webp": "WEBP",
        "heif": "HEIF",
        "avif": "AVIF",
        "gif": "GIF",
    }
    
    # Regex patterns for codec identification
    _CODEC_PATTERNS: List[Tuple[str, str, str]] = [
        # Video codec patterns
        (r'^avc(1|3)?.*$', 'video', 'H264'),
        (r'^AVC(1|3)?.*$', 'video', 'H264'),
        (r'^(hev|hvc)1?.*$', 'video', 'H265'),
        (r'^(dvh|dvhe)1?.*$', 'video', 'DOVI'),
        (r'^vp(09|9)(\.[0-9])?$', 'video', 'VP9'),
        (r'^av(01|1)(\.[0-9])?.*$', 'video', 'AV1'),
        
        # Audio codec patterns
        (r'^mp4a\.40\.[0-9]+$', 'audio', 'AAC'),
        (r'^mp4a\.6[0-9a-fA-F]$', 'audio', 'MP3'),
        (r'^mp4a\.[aA][0-9a-fA-F]$', 'audio', 'DOLBY'),
        (r'^mp4a\.[aA][cC]$', 'audio', 'DTS_HD'),
        (r'^mp4a\.[aA][9]$', 'audio', 'DTS'),
        (r'^dts-.*$', 'audio', 'DTS'),
        (r'^ec3$', 'audio', 'EAC3'),
    ]
    
    # Container format detection
    _CONTAINER_FORMATS: Dict[str, str] = {
        "mp4": "MP4",
        "webm": "WEBM",
        "mkv": "MATROSKA",
        "mov": "QUICKTIME",
        "avi": "AVI",
        "flv": "FLASH_VIDEO",
        "ts": "MPEG_TS",
        "m3u8": "HLS",
        "mpd": "DASH",
        "ism": "SMOOTH_STREAMING",
    }
    
    log = Logger('CodecPy')
    
    def __init__(self):
        """
        Initialize the CodecPy library
        """
    
    @classmethod
    def normalize_codec(cls, codec_string: str, codec_type: Optional[str] = None) -> CodecInfo:
        """
        Normalize a codec string to a human-readable format with additional metadata.
        
        Args:
            codec_string: The codec string to normalize
            codec_type: Optional type hint ('audio', 'video', 'text', 'image')
            
        Returns:
            CodecInfo object containing normalized information about the codec
        """
        if codec_string is None:
            return CodecInfo.create_unknown()
        
        # Lowercase for consistent processing
        codec_orig = codec_string
        codec_string = codec_string.lower()
        
        # Try direct mapping first
        result = None
        detected_type = codec_type
        
        # Find in maps
        if not detected_type or detected_type == 'audio':
            if codec_string in cls._AUDIO_CODEC_MAP:
                result = cls._AUDIO_CODEC_MAP[codec_string]
                detected_type = 'audio'
        
        if (not result and (not detected_type or detected_type == 'video')):
            if codec_string in cls._VIDEO_CODEC_MAP:
                result = cls._VIDEO_CODEC_MAP[codec_string]
                detected_type = 'video'
                
        if (not result and (not detected_type or detected_type == 'text')):
            if codec_string in cls._TEXT_CODEC_MAP:
                result = cls._TEXT_CODEC_MAP[codec_string]
                detected_type = 'text'
                
        if (not result and (not detected_type or detected_type == 'image')):
            if codec_string in cls._IMAGE_CODEC_MAP:
                result = cls._IMAGE_CODEC_MAP[codec_string]
                detected_type = 'image'
        
        # Try pattern matching if direct mapping failed
        if not result:
            for pattern, pattern_type, mapped_value in cls._CODEC_PATTERNS:
                if re.match(pattern, codec_orig, re.IGNORECASE):
                    result = mapped_value
                    detected_type = pattern_type
                    break
        
        # Build detailed codec info
        if result:
            family = result.split('_')[0] if '_' in result else result
            
            # Handle special cases for technical ID
            if detected_type == 'audio' and 'AAC' in result:
                technical_id = 'mp4a.40'
            elif detected_type == 'audio' and 'DTS' in result:
                technical_id = 'mp4a.a9' if result == 'DTS' else 'mp4a.ac'
            elif detected_type == 'audio' and result == 'EAC3':
                technical_id = 'ec-3'
            elif detected_type == 'video' and result == 'H264':
                technical_id = 'avc1'
            elif detected_type == 'video' and result == 'H265':
                technical_id = 'hvc1'
            else:
                technical_id = codec_string
                
            return CodecInfo(
                original=codec_orig,
                normalized=result,
                type=CodecType.from_string(detected_type),
                technical_id=technical_id,
                family=family
            )
        
        # Return best-effort if no match found
        return CodecInfo(
            original=codec_orig,
            normalized=codec_string.upper(),
            type=CodecType.from_string(detected_type or 'unknown'),
            technical_id=codec_string,
            family=None
        )
    
    @classmethod
    def decode_codec_string(cls, codec_string: str) -> CodecStreamInfo:
        """
        Comprehensively decode a complex codec string into component parts
        
        Args:
            codec_string: The codec string to decode (can be complex like 'avc1.640028, mp4a.40.2')
            
        Returns:
            CodecStreamInfo object with detailed codec information
        """
        result = CodecStreamInfo(
            original=codec_string,
            codecs=[],
            has_video=False,
            has_audio=False,
            has_text=False
        )
        
        if not codec_string:
            return result
            
        # Handle multiple codec strings (comma-separated)
        codec_parts = [part.strip() for part in codec_string.split(',')]
        
        for codec in codec_parts:
            codec_info = cls.normalize_codec(codec)
            result.codecs.append(codec_info)
            
            if codec_info.type == CodecType.VIDEO:
                result.has_video = True
                result.video_codec = codec_info.normalized
            elif codec_info.type == CodecType.AUDIO:
                result.has_audio = True
                result.audio_codec = codec_info.normalized
            elif codec_info.type == CodecType.TEXT:
                result.has_text = True
        
        return result
    
    @classmethod
    def identify_container(cls, file_extension: str) -> ContainerInfo:
        """
        Identify container format from file extension
        
        Args:
            file_extension: File extension (e.g. 'mp4', 'webm')
            
        Returns:
            ContainerInfo object with format information
        """
        ext = file_extension.lower().lstrip('.')
        
        if ext in cls._CONTAINER_FORMATS:
            name = cls._CONTAINER_FORMATS[ext]
            return ContainerInfo(
                extension=ext,
                format=name,
                type='container'
            )
        
        return ContainerInfo(
            extension=ext,
            format='UNKNOWN',
            type='unknown'
        )
    
    @classmethod
    def get_compatible_codecs(cls, container: str) -> Dict[str, List[str]]:
        """
        Get list of codecs compatible with a specific container
        
        Args:
            container: Container format (e.g. 'mp4', 'webm')
            
        Returns:
            Dictionary of compatible audio and video codecs
        """
        container = container.lower().lstrip('.')
        
        # Define compatibility matrix
        compatibility = {
            'mp4': {
                'video': ['H264', 'H265', 'AV1', 'VP9', 'MPEG4'],
                'audio': ['AAC', 'MP3', 'AC3', 'EAC3', 'FLAC', 'ALAC', 'DTS', 'DTS_HD', 'DTS_HD_MA'],
            },
            'webm': {
                'video': ['VP8', 'VP9', 'AV1'],
                'audio': ['VORBIS', 'OPUS'],
            },
            'mkv': {
                'video': ['H264', 'H265', 'VP8', 'VP9', 'AV1', 'THEORA'],
                'audio': ['AAC', 'MP3', 'AC3', 'EAC3', 'FLAC', 'VORBIS', 'OPUS', 'DTS', 'DTS_HD', 'DTS_HD_MA', 'DTS_X'],
            },
        }
        
        if container in compatibility:
            return compatibility[container]
        
        return {
            'video': [],
            'audio': []
        }
    
    @staticmethod
    def fix_codecs(codec_string: str) -> str:
        """
        Legacy compatibility method that normalizes a codec string to human-readable format
        
        Args:
            codec_string: The codec string to normalize
            
        Returns:
            Normalized human-readable codec name
        """
        if not codec_string:
            return None
            
        result = CodecPy.normalize_codec(codec_string)
        return result.normalized
        
    @classmethod
    def parse_profiles(cls, codec_string: str) -> ProfileInfo:
        """
        Extract profile and level information from complex codec strings
        
        Args:
            codec_string: Codec string potentially containing profile info
            
        Returns:
            ProfileInfo object with profile and level information
        """
        result = ProfileInfo(original=codec_string)
        
        if not codec_string:
            return result
            
        # Handle H.264 profiles (avc1.PPCCLL format)
        if codec_string.startswith(('avc1.', 'avc3.')):
            try:
                parts = codec_string.split('.')
                if len(parts) < 2 or not parts[1]:
                    return result
                    
                profile_part = parts[1]
                if len(profile_part) >= 6:
                    # Use uppercase for consistency in profile code matching
                    profile_code = profile_part[0:2].upper()
                    constraint_code = profile_part[2:4]
                    level_code = profile_part[4:6]
                    
                    # Map profile codes - case insensitive handling
                    profile_map = {
                        '42': 'Baseline',
                        '4D': 'Main',
                        '58': 'Extended',
                        '64': 'High',
                        '6E': 'High 10',
                        '7A': 'High 4:2:2',
                        'F4': 'High 4:4:4',
                        # Additional common profiles
                        '53': 'Scalable Baseline',
                        '56': 'Scalable High',
                        '76': 'Multiview High',
                        '80': 'Stereo High',
                    }
                    
                    # Map constraint flags - bits meaning in constraint_code
                    constraint_flags = []
                    constraint_int = int(constraint_code, 16)
                    if constraint_int & 0x80:
                        constraint_flags.append("constraint_set0_flag")
                    if constraint_int & 0x40:
                        constraint_flags.append("constraint_set1_flag")
                    if constraint_int & 0x20:
                        constraint_flags.append("constraint_set2_flag")
                    if constraint_int & 0x10:
                        constraint_flags.append("constraint_set3_flag")
                    
                    result.has_profile = True
                    result.profile = profile_map.get(profile_code, f"Unknown ({profile_code})")
                    result.level = float(int(level_code, 16)) / 10
                    result.constraints = constraint_code
                    result.constraint_flags = constraint_flags
                    
                    # Add detailed profile info
                    if result.profile == "High" and "constraint_set3_flag" in constraint_flags:
                        result.profile_details = "High with additional compatibility constraints"
            except Exception as e:
                cls.log.debug(f"Error parsing AVC profile: {str(e)}")
                
        # Handle H.265/HEVC profiles with improved parsing
        elif codec_string.startswith(('hvc1.', 'hev1.')):
            parts = codec_string.split('.')
            if len(parts) >= 2:
                try:
                    # Format: hvc1.1.6.L150.B0 or hvc1.1.6.H150.B0
                    if len(parts) >= 4 and any(parts[3].startswith(x) for x in ['L', 'H']):
                        tier_indicator = parts[3][0]
                        level_value = parts[3][1:]
                        
                        # Profile space and profile index mapping
                        profile_spaces = {
                            '0': "General",
                            '1': "Extended",
                            '2': "Main",
                            '3': "Reserved"
                        }
                        
                        hevc_profiles = {
                            '1': "Main",
                            '2': "Main 10",
                            '3': "Main Still Picture",
                            '4': "RExt",
                            '5': "High Throughput",
                            '6': "MV-HEVC",
                            '7': "Scalable Main",
                            '8': "3D Main",
                            '9': "SCC",
                        }
                        
                        result.has_profile = True
                        result.profile_space = profile_spaces.get(parts[1], f"Unknown ({parts[1]})")
                        result.profile = hevc_profiles.get(parts[2], f"Profile {parts[2]}")
                        result.tier = 'High' if tier_indicator == 'H' else 'Main'
                        result.level = float(level_value) / 30
                        
                        # Extract compatibility flags if present
                        if len(parts) >= 5 and parts[4].startswith('B'):
                            result.compatibility_flags = parts[4][1:]
                except Exception as e:
                    cls.log.debug(f"Error parsing HEVC profile: {str(e)}")
        
        # Handle VP9 profiles
        elif codec_string.startswith('vp09.'):
            try:
                parts = codec_string.split('.')
                if len(parts) >= 4:
                    profile_code = parts[1]
                    level_code = parts[2]
                    
                    vp9_profiles = {
                        '00': 'Profile 0 (8-bit, 4:2:0)',
                        '01': 'Profile 1 (8-bit, 4:2:2/4:4:4)',
                        '02': 'Profile 2 (10/12-bit, 4:2:0)',
                        '03': 'Profile 3 (10/12-bit, 4:2:2/4:4:4)'
                    }
                    
                    result.has_profile = True
                    result.profile = vp9_profiles.get(profile_code, f"Unknown ({profile_code})")
                    result.level = float(level_code) / 10
                    result.bit_depth = parts[3]
            except Exception as e:
                cls.log.debug(f"Error parsing VP9 profile: {str(e)}")
        
        # Handle AAC profiles with expanded support
        elif codec_string.startswith('mp4a.40.'):
            try:
                profile_code = codec_string.split('.')[2]
                profile_map = {
                    '1': 'AAC Main',
                    '2': 'AAC-LC',
                    '3': 'AAC SSR',
                    '4': 'AAC LTP',
                    '5': 'HE-AAC / SBR',
                    '6': 'AAC Scalable',
                    '22': 'ER AAC-LC',
                    '29': 'HE-AACv2 / SBR+PS',
                    '39': 'AAC-ELD',
                    '42': 'XHE-AAC',
                }
                result.has_profile = True
                result.profile = profile_map.get(profile_code, f"Unknown ({profile_code})")
                result.codec_family = "AAC"
            except Exception as e:
                cls.log.debug(f"Error parsing AAC profile: {str(e)}")
                
        # Handle DTS profiles with extended versions
        elif codec_string.startswith('dts'):
            try:
                if '-' in codec_string:
                    dts_type = codec_string.split('-')[1].lower()
                    profile_map = {
                        'hd': 'High Definition',
                        'hdma': 'HD Master Audio',
                        'hdhr': 'HD High Resolution Audio',
                        'x': 'DTS:X',
                        'xll': 'DTS:X Lossless',
                        'express': 'Express',
                        'es': 'Extended Surround',
                        '96/24': '96/24',
                    }
                    result.has_profile = True
                    result.profile = profile_map.get(dts_type, "Core")
                else:
                    result.has_profile = True
                    result.profile = "Core"
                result.codec_family = "DTS"
            except Exception as e:
                cls.log.debug(f"Error parsing DTS profile: {str(e)}")
        
        # Handle Dolby profiles
        elif codec_string.startswith(('ec-3', 'ec3', 'ac-3', 'mlpa')):
            try:
                # Standardize the dolby type for both ec-3 and ec3 variants
                dolby_type = codec_string.split('.')[0].lower()
                if dolby_type == 'ec3':
                    dolby_type = 'ec-3'
                    
                profile_map = {
                    'ec-3': 'Dolby Digital Plus (E-AC-3)',
                    'ac-3': 'Dolby Digital (AC-3)',
                    'mlpa': 'Dolby TrueHD',
                }
                result.has_profile = True
                result.profile = profile_map.get(dolby_type)
                result.codec_family = "Dolby"
            except Exception as e:
                cls.log.debug(f"Error parsing Dolby profile: {str(e)}")
                
        return result

    @staticmethod
    def parse_channel_format(channels: Union[str, float, int]) -> Optional[str]:
        """
        Converts channel representation to a human-readable format.
        Handles numeric values, common layout codes, and special format strings.
        
        Args:
            channels: Channel specification as string, float, or integer
            
        Returns:
            Human-readable channel format (e.g. "2.0", "5.1", "7.1")
        """
        # Handle None or empty string
        if channels is None or channels == "":
            return None
        
        # Handle common industry codes
        channel_codes = {
            "A000": "2.0",    # Stereo
            "F801": "5.1",    # 5.1 surround
            "FA01": "7.1",    # 7.1 surround
            "15/JOC": "16.0", # Dolby Atmos with Joint Object Coding
            "22.2": "22.2",   # NHK 22.2
            "3/0/0": "3.0",   # L/C/R
            "5/0/0": "5.0",   # L/C/R/Ls/Rs
            "5/0/2": "5.2",   # L/C/R/Ls/Rs + 2 LFE
            "4/0/0": "4.0",   # Quadraphonic
            "7/0/2": "7.2",   # 7.2 surround
            "9/0/4": "9.4"    # 9.4 surround
        }
        
        if isinstance(channels, str) and channels in channel_codes:
            return channel_codes[channels]
        
        # Handle channel specifications with format X.Y
        if isinstance(channels, str) and "/" in channels and not channels.endswith("/JOC"):
            # Format might be front/side/back or front/side/LFE
            parts = channels.split("/")
            if len(parts) == 3:
                try:
                    total = int(parts[0]) + int(parts[1]) + int(parts[2])
                    if int(parts[2]) > 0:
                        # If last part is LFE
                        return f"{int(parts[0]) + int(parts[1])}.{parts[2]}"
                    else:
                        return f"{total}.0"
                except ValueError:
                    pass
        
        # Handle integer values - return as X.0
        if isinstance(channels, int) or (isinstance(channels, str) and channels.isdigit()):
            return f"{int(channels)}.0"
        
        # Handle float values - ensure proper format
        try:
            if isinstance(channels, float) or (isinstance(channels, str) and "." in channels):
                channel_float = float(channels)
                main, sub = str(channel_float).split(".")
                return f"{main}.{sub}"
        except ValueError:
            pass
        
        # Return as is for unrecognized formats
        return str(channels)
    
    @classmethod
    def get_audio_codec_details(cls, codec_string: str, channels: Optional[Union[str, float, int]] = None,
                            sample_rate: Optional[int] = None, bit_depth: Optional[int] = None, base_only: Optional[bool] = False) -> AudioCodecDetails:
        """
        Get comprehensive information about an audio codec with channel configuration details.
        
        Args:
            codec_string: The audio codec string to analyze
            channels: Channel specification (can be code, number, or format string)
            sample_rate: Optional sample rate in Hz
            bit_depth: Optional bit depth
            
        Returns:
            AudioCodecDetails object with all available codec information
        """
        base_details = cls.get_codec_details(codec_string)
        
        # Only process as audio if the codec is actually an audio codec
        if base_only and base_details.type != CodecType.AUDIO:
            return base_details
        
        return AudioCodecDetails(
            original=base_details.original,
            normalized=base_details.normalized,
            type=base_details.type,
            family=base_details.family,
            profiles=base_details.profiles,
            color_info=None,
            channels=cls.parse_channel_format(channels),
            sample_rate=sample_rate,
            bit_depth=bit_depth
        )
        
    @classmethod
    def get_codec_details(cls, codec_string: str) -> CodecDetails:
        """
        Comprehensive method to get all available information about a codec string
        
        Args:
            codec_string: The codec string to analyze
            
        Returns:
            CodecDetails object with all available codec information
        """
        base_info = cls.normalize_codec(codec_string)
        profile_info = cls.parse_profiles(codec_string)
        
        result = CodecDetails(
            original=codec_string,
            normalized=base_info.normalized,
            type=base_info.type,
            family=base_info.family,
            profiles=profile_info if profile_info.has_profile else None,
        )
        
        # Add codec-specific additional information
        if base_info.type == CodecType.VIDEO:
            result.color_info = cls._detect_color_info(codec_string)
            
        return result
    
    @staticmethod
    def _detect_color_info(codec_string: str) -> ColorInfo:
        """
        Detect color information from codec string
        
        Args:
            codec_string: Video codec string that may contain color info
            
        Returns:
            ColorInfo object with color information if available
        """
        # This is a placeholder for color information detection
        # In a full implementation, this would parse color primaries, transfer characteristics, etc.
        return ColorInfo(detected=False)
    
    @classmethod
    def batch_process_codecs(cls, codec_strings: List[str]) -> List[CodecDetails]:
        """
        Process multiple codec strings at once
        
        Args:
            codec_strings: List of codec strings to process
            
        Returns:
            List of CodecDetails objects with normalized codec information
        """
        return [cls.get_codec_details(codec) for codec in codec_strings]
    
    @classmethod
    def is_codec_compatible(cls, codec: str, container: str) -> bool:
        """
        Check if a codec is compatible with a specific container
        
        Args:
            codec: Codec string to check
            container: Container format string
            
        Returns:
            Boolean indicating compatibility
        """
        codec_info = cls.normalize_codec(codec)
        compatible_codecs = cls.get_compatible_codecs(container)
        
        if codec_info.type == CodecType.VIDEO:
            return codec_info.normalized in compatible_codecs['video']
        elif codec_info.type == CodecType.AUDIO:
            return codec_info.normalized in compatible_codecs['audio']
            
        return False
    
    @classmethod
    def suggest_container(cls, video_codec: str, audio_codec: str) -> List[str]:
        """
        Suggest compatible containers for a video/audio codec combination
        
        Args:
            video_codec: Video codec string
            audio_codec: Audio codec string
            
        Returns:
            List of compatible container formats
        """
        video_info = cls.normalize_codec(video_codec, 'video') if video_codec else None
        audio_info = cls.normalize_codec(audio_codec, 'audio') if audio_codec else None
        
        compatible_containers = []
        
        for container in ['mp4', 'webm', 'mkv']:
            compat = cls.get_compatible_codecs(container)
            
            video_compatible = (not video_info) or (video_info.normalized in compat['video'])
            audio_compatible = (not audio_info) or (audio_info.normalized in compat['audio'])
            
            if video_compatible and audio_compatible:
                compatible_containers.append(container)
                
        return compatible_containers

    @classmethod
    def process_mime_type(cls, mime_type_str: str) -> Tuple[str, List[CodecInfo]]:
        """
        Process a MIME type string to extract and normalize any codec information
        
        Args:
            mime_type_str: MIME type string potentially with codecs parameter
            
        Returns:
            Tuple of (container_type, list of CodecInfo objects)
        """
        mime_info = MimeTypeUtil.parse_mime_type(mime_type_str)
        codecs_list = mime_info.codecs_parameter or []
        
        # Determine codec type hint from MIME type
        codec_type_hint = MimeTypeUtil.get_codec_type_from_mime(mime_type_str)
        
        # Process codecs
        codec_infos = []
        for codec_str in codecs_list:
            codec_info = cls.normalize_codec(codec_str, codec_type_hint)
            codec_infos.append(codec_info)
            
        return mime_info.full_type, codec_infos
    
    @classmethod
    def create_mime_type_for_codecs(cls, container: str, video_codec: Optional[str] = None, 
                                  audio_codec: Optional[str] = None) -> str:
        """
        Create a MIME type string for container and codec combination
        
        Args:
            container: Container format (e.g. 'mp4', 'webm')
            video_codec: Optional video codec string
            audio_codec: Optional audio codec string
            
        Returns:
            MIME type string with codecs parameter
        """
        base_mime = MimeTypeUtil.get_mime_type_for_extension(container)
        
        codecs = []
        if video_codec:
            video_info = cls.normalize_codec(video_codec, 'video')
            codecs.append(video_info.technical_id)
            
        if audio_codec:
            audio_info = cls.normalize_codec(audio_codec, 'audio')
            codecs.append(audio_info.technical_id)
            
        return MimeTypeUtil.create_mime_type_with_codecs(base_mime, codecs)
    
    @classmethod
    def get_compatible_mime_types(cls, codec_string: str) -> List[str]:
        """
        Get compatible MIME types for a codec
        
        Args:
            codec_string: Codec string to check compatibility for
            
        Returns:
            List of compatible MIME types
        """
        codec_info = cls.normalize_codec(codec_string)
        compatible_mime_types = []
        
        if codec_info.type == CodecType.VIDEO:
            # Check compatibility with video containers
            for container in ['mp4', 'webm', 'mkv']:
                if cls.is_codec_compatible(codec_string, container):
                    mime_type = MimeTypeUtil.get_mime_type_for_extension(container)
                    compatible_mime_types.append(mime_type)
                    
        elif codec_info.type == CodecType.AUDIO:
            # Check compatibility with audio containers
            for container in ['mp4', 'webm', 'ogg', 'mp3', 'wav']:
                if cls.is_codec_compatible(codec_string, container):
                    mime_type = MimeTypeUtil.get_mime_type_for_extension(container)
                    compatible_mime_types.append(mime_type)
        
        return compatible_mime_types


if __name__ == "__main__":
    test_codecs = [
        "avc1.640028", 
        "mp4a.40.2",
        "hev1.1.6.L150.B0",
        "vp9.2",
        "dts",
        "dts-hd",
        "dts-hdma",
        "mp4a.a9",
        "mp4a.ac"
    ]
    
    for codec in test_codecs:
        result = CodecPy.get_codec_details(codec)
        print(f"Original: {codec}")
        print(f"Normalized: {result.normalized}")
        print(f"Type: {result.type.to_string()}")
        if result.profiles and result.profiles.has_profile:
            print(f"Profile: {result.profiles.profile}")
        print("---")
        
    print("--- MIME ---")
    # Example usage of MIME type functionality
    # Parse MIME type with codecs
    mime_str = 'video/mp4; codecs="avc1.640028, mp4a.40.2"'
    mime_info = MimeTypeUtil.parse_mime_type(mime_str)
    print(f"Main type: {mime_info.main_type}")
    print(f"Sub type: {mime_info.sub_type}")
    print(f"Codecs: {mime_info.codecs_parameter}")
    
    # Process MIME type with CodecPy
    container, codecs = CodecPy.process_mime_type(mime_str)
    print(f"Container: {container}")
    for codec in codecs:
        print(f"Codec: {codec.normalized} (Type: {codec.type.to_string()})")
    
    # Create MIME type for codecs
    mime_type = CodecPy.create_mime_type_for_codecs('mp4', 'avc1.640028', 'mp4a.40.2')
    print(f"Generated MIME type: {mime_type}")
