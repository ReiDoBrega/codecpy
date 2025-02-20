from typing import Optional
from dataclasses import dataclass

@dataclass
class ProfileInfo:
    """Class representing codec profile information"""
    original: str
    has_profile: bool = False
    profile: Optional[str] = None
    level: Optional[float] = None
    tier: Optional[str] = None
    constraints: Optional[str] = None

