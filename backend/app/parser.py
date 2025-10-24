# backend/app/parser.py
from datetime import datetime
import xml.etree.ElementTree as ET
import csv
from typing import List, Dict

def parse_xml_body_lines(xml_content: str) -> List[Dict]:
    """
    Parses an XML where <body> contains tab-delimited rows (like your sample).
    Returns list of dicts per row.
    """
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError:
        return []

    body = root.find('.//body')
    if body is None:
        # try to use full text if body not a node with inner text
        text = ''.join(root.itertext())
    else:
        text = ''.join(body.itertext())

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    docs = []
    for line in lines:
        parts = line.split("\t")
        if len(parts) >= 9:
            content = "\t".join(parts[9:]) if len(parts) > 9 else ""
            doc = {
                "source": parts[0],
                "pattern": parts[1],
                "num1": parts[2],
                "num2": parts[3],
                "flag1": parts[4],
                "flag2": parts[5],
                "datetime_raw": parts[6],
                "user": parts[7],
                "title": parts[8],
                "content": content
            }
            try:
                doc["datetime"] = datetime.strptime(doc["datetime_raw"], "%d/%m/%Y %H:%M:%S")
            except Exception:
                doc["datetime"] = None
            docs.append(doc)
        else:
            docs.append({"raw_line": line})
    return docs

def parse_csv_content(csv_text: str) -> List[Dict]:
    reader = csv.DictReader(csv_text.splitlines())
    return [row for row in reader]
