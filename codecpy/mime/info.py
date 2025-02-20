from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class MimeTypeInfo:
    """Class representing MIME type information"""
    full_type: str
    main_type: str
    sub_type: str
    parameters: Dict[str, str]
    
    @property
    def codecs_parameter(self) -> Optional[List[str]]:
        """Extract and parse codecs parameter if present"""
        if 'codecs' not in self.parameters:
            return None
        
        codecs = self.parameters['codecs']
        if codecs.startswith('"') and codecs.endswith('"'):
            codecs = codecs[1:-1]
        
        return [c.strip() for c in codecs.split(',')]

