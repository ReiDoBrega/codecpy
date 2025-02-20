from codecpy import CodecPy# Example usage
codex = CodecPy()

# Basic audio codec identification
aac_info = codex.normalize_codec("mp4a.40.2", "audio")
print(f"Codec: {aac_info.normalized}")  # Outputs: "Codec: AAC_LC"

# Detailed audio codec information with channels
ac3_details = codex.get_audio_codec_details("ac-3", "F801", 48000, 16)
print(f"Audio: {ac3_details.normalized} {ac3_details.channels}")  # Outputs: "Audio: AC3 5.1"

# Process from string representation
atmos_details = codex.get_audio_codec_details("ec-3", "15/JOC", 48000)
print(f"Format: {atmos_details.normalized} Atmos {atmos_details.channels}")  # Outputs: "Format: EAC3 Atmos 16.0"