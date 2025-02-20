from typing import Optional
from dataclasses import dataclass

@dataclass
class ColorInfo:
    """Class representing video color information"""
    detected: bool = False
    bit_depth: Optional[int] = None
    color_primaries: Optional[str] = None
    transfer_characteristics: Optional[str] = None
    matrix_coefficients: Optional[str] = None
