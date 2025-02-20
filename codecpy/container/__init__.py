
from dataclasses import dataclass


@dataclass
class ContainerInfo:
    """Class representing container format information"""
    extension: str
    format: str
    type: str

