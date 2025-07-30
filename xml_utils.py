import base64
import xml.etree.ElementTree as ET
from typing import List
from xml_models import Part


def find_parts(file_path: str) -> List[Part]:
    root = ET.parse(file_path).getroot()
    parts = []
    for part_elem in root.iter("Part"):
        part = Part(
            id=part_elem.get("id"),
            filename=part_elem.findtext("Filename"),
            type=part_elem.findtext("Type"),
            body=base64.b64decode(part_elem.findtext("Body")),
        )
        parts.append(part)
    return parts
