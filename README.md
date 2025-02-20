# CodecPy 📊

![CodecPy Logo](https://raw.githubusercontent.com/ReiDoBrega/codecpy/main/assets/logo.png)

A professional Python library for processing and normalizing media codec strings to human-readable formats. CodecPy handles a wide range of audio and video codecs with comprehensive mapping and pattern recognition.

[![PyPI version](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](https://pypi.org/project/codecpy/)
[![Python versions](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Features

- Normalize complex codec strings into human-readable formats
- Identify and classify audio, video, text, and image codecs
- Extract profile, level, and color information from codec strings
- Parse and create MIME types with codec parameters
- Determine codec compatibility with various container formats
- Suggest optimal containers for codec combinations

## Installation

```bash
pip install codecpy
```

## Quick Start

```python
from codecpy import CodecPy

# Basic codec normalization
codec_info = CodecPy.normalize_codec("avc1.640028")
print(f"Normalized codec: {codec_info.normalized}")  # Output: Normalized codec: H264

# Process MIME type with codecs
mime_str = 'video/mp4; codecs="avc1.640028, mp4a.40.2"'
codec_stream = CodecPy.decode_codec_string("avc1.640028, mp4a.40.2")
print(f"Video codec: {codec_stream.video_codec}")  # Output: Video codec: H264
print(f"Audio codec: {codec_stream.audio_codec}")  # Output: Audio codec: AAC_LC
```

## Documentation

### Core Classes

- `CodecInfo`: Normalized codec information
- `ProfileInfo`: Codec profile and level details
- `ColorInfo`: Video color space information
- `CodecDetails`: Comprehensive codec details
- `ContainerInfo`: Container format information
- `CodecStreamInfo`: Multi-codec stream information
- `MimeTypeInfo`: MIME type parsing results

### Basic Usage

#### Normalize a Codec

```python
from codecpy import CodecPy

# Normalize a video codec
codec_info = CodecPy.normalize_codec("avc1.640028")
print(f"Original: {codec_info.original}")
print(f"Normalized: {codec_info.normalized}")
print(f"Type: {codec_info.type.to_string()}")
print(f"Technical ID: {codec_info.technical_id}")
print(f"Family: {codec_info.family}")
```

Output:
```
Original: avc1.640028
Normalized: H264
Type: video
Technical ID: avc1
Family: H264
```

#### Get Detailed Codec Information

```python
# Get comprehensive codec details including profile information
details = CodecPy.get_codec_details("avc1.640028")
print(f"Codec: {details.normalized}")
if details.profiles and details.profiles.has_profile:
    print(f"Profile: {details.profiles.profile}")
    print(f"Level: {details.profiles.level}")
```

Output:
```
Codec: H264
Profile: High
Level: 4.0
```

#### Process Multiple Codecs in a Stream

```python
# Process a codec string with multiple codecs
codec_stream = CodecPy.decode_codec_string("avc1.640028, mp4a.40.2")
print(f"Has video: {codec_stream.has_video}")
print(f"Has audio: {codec_stream.has_audio}")
print(f"Video codec: {codec_stream.video_codec}")
print(f"Audio codec: {codec_stream.audio_codec}")

# Get individual codec details
for codec in codec_stream.codecs:
    print(f"- {codec.type.to_string()}: {codec.normalized}")
```

Output:
```
Has video: True
Has audio: True
Video codec: H264
Audio codec: AAC_LC
- video: H264
- audio: AAC_LC
```

### MIME Type Handling

#### Parse a MIME Type

```python
from codecpy.mime import MimeTypeUtil

mime_str = 'video/mp4; codecs="avc1.640028, mp4a.40.2"'
mime_info = MimeTypeUtil.parse_mime_type(mime_str)

print(f"Full type: {mime_info.full_type}")
print(f"Main type: {mime_info.main_type}")
print(f"Sub type: {mime_info.sub_type}")
print(f"Codecs: {mime_info.codecs_parameter}")
```

Output:
```
Full type: video/mp4
Main type: video
Sub type: mp4
Codecs: ['avc1.640028', 'mp4a.40.2']
```

#### Process MIME Type with Codecs

```python
# Process MIME type with CodecPy
container, codecs = CodecPy.process_mime_type(mime_str)
print(f"Container: {container}")
for codec in codecs:
    print(f"- {codec.type.to_string()}: {codec.normalized}")
```

Output:
```
Container: video/mp4
- video: H264
- audio: AAC_LC
```

#### Create MIME Type for Codec Combination

```python
# Create a MIME type string for a video/audio codec pair
mime_type = CodecPy.create_mime_type_for_codecs('mp4', 'avc1.640028', 'mp4a.40.2')
print(f"Generated MIME type: {mime_type}")
```

Output:
```
Generated MIME type: video/mp4; codecs="avc1, mp4a.40.2"
```

### Container Compatibility

#### Check Codec Compatibility

```python
# Check if a codec is compatible with a container
is_compatible = CodecPy.is_codec_compatible("avc1.640028", "mp4")
print(f"H.264 compatible with MP4: {is_compatible}")

is_compatible = CodecPy.is_codec_compatible("vp9", "mp4")
print(f"VP9 compatible with MP4: {is_compatible}")
```

Output:
```
H.264 compatible with MP4: True
VP9 compatible with MP4: True
```

#### Suggest Compatible Containers

```python
# Get container suggestions for codec combination
containers = CodecPy.suggest_container("h265", "aac")
print(f"Compatible containers for H.265 + AAC: {containers}")
```

Output:
```
Compatible containers for H.265 + AAC: ['mp4', 'mkv']
```

### Advanced Usage: Detailed Profile Information

```python
# Extract profile and level information from complex codec strings
test_codecs = [
    "avc1.640028",
    "hev1.1.6.L150.B0",
    "vp9.2",
    "mp4a.40.2",
    "dts-hdma"
]

for codec in test_codecs:
    result = CodecPy.get_codec_details(codec)
    print(f"\nOriginal: {codec}")
    print(f"Normalized: {result.normalized}")
    print(f"Type: {result.type.to_string()}")
    if result.profiles and result.profiles.has_profile:
        print(f"Profile: {result.profiles.profile}")
        if result.profiles.level:
            print(f"Level: {result.profiles.level}")
```

Output:
```
Original: avc1.640028
Normalized: H264
Type: video
Profile: High
Level: 4.0

Original: hev1.1.6.L150.B0
Normalized: H265
Type: video
Profile: Profile 1
Tier: High
Level: 5.0

Original: vp9.2
Normalized: VP9_PROFILE_2
Type: video

Original: mp4a.40.2
Normalized: AAC_LC
Type: audio
Profile: AAC-LC

Original: dts-hdma
Normalized: DTS_HD_MA
Type: audio
Profile: HD Master Audio
```

## Batch Processing

```python
# Process multiple codec strings in one call
results = CodecPy.batch_process_codecs([
    "avc1.640028",
    "mp4a.40.2",
    "vp9.2"
])

for result in results:
    print(f"{result.original} → {result.normalized} ({result.type.to_string()})")
```

Output:
```
avc1.640028 → H264 (video)
mp4a.40.2 → AAC_LC (audio)
vp9.2 → VP9_PROFILE_2 (video)
```

## Debugging

Enable debug mode for detailed logging:

```python
codex = CodecPy(debug_mode=True)
# Now all operations will produce detailed logs
```

## Common Use Cases

### Media Player Development

```python
# Determine if a media file can be played based on codec support
video_codec = "avc1.640028"
audio_codec = "mp4a.40.2"
container = "mp4"

can_play_video = CodecPy.is_codec_compatible(video_codec, container)
can_play_audio = CodecPy.is_codec_compatible(audio_codec, container)

if can_play_video and can_play_audio:
    print("Media file can be played")
else:
    print("Unsupported format")
```

### Streaming Media Server

```python
# Generate compatible MIME types for adaptive streaming manifests
video_codec = "avc1.640028"
audio_codec = "mp4a.40.2"

mime_type = CodecPy.create_mime_type_for_codecs('mp4', video_codec, audio_codec)
print(f"DASH/HLS MIME type: {mime_type}")
```

### Media Analytics

```python
# Parse codec information from media files for analytics
media_files = [
    "video1.mp4;avc1.640028,mp4a.40.2",
    "video2.webm;vp9,opus",
    "audio1.m4a;mp4a.40.2"
]

for file_info in media_files:
    container, codec_str = file_info.split(';')
    ext = container.split('.')[-1]
    codec_stream = CodecPy.decode_codec_string(codec_str)
    
    print(f"\nAnalyzing: {container}")
    print(f"Container: {CodecPy.identify_container(ext).format}")
    
    if codec_stream.has_video:
        print(f"Video codec: {codec_stream.video_codec}")
    if codec_stream.has_audio:
        print(f"Audio codec: {codec_stream.audio_codec}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [FFmpeg](https://ffmpeg.org/) - For reference codec implementation details
- [W3C Media Source Extensions](https://w3c.github.io/media-source/) - For codec string format specifications

---

Made with ❤️ for media developers