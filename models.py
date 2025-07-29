

from dataclasses import dataclass
@dataclass
class Part:
    id: str
    filename: str
    type: str
    body: bytes