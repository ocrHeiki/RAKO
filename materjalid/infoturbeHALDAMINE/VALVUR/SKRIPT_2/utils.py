#!/usr/bin/env python3
import os
import sys
import logging
import platform
import socket
from datetime import datetime

class ValvurEvent:
    def __init__(self, timestamp, source, event_id, severity, description, mitre_id="N/A"):
        self.timestamp = timestamp
        self.source = source
        self.event_id = event_id
        self.severity = severity
        self.description = description
        self.mitre_id = mitre_id

    def to_dict(self):
        return {
            "Aeg": self.timestamp,
            "Allikas": self.source,
            "ID": self.event_id,
            "Tase": self.severity,
            "Kirjeldus": self.description,
            "MITRE": self.mitre_id
        }

def get_output_dir():
    """Tagastab ühtse väljundkausta (Punkt 3)."""
    # Kui MASTER on määranud asukoha, kasutame seda, muidu vaikimisi TULEMUSED
    out_dir = os.environ.get("VALVUR_OUT")
    if not out_dir:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        out_dir = os.path.join(base_dir, "TULEMUSED")
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    return out_dir

def setup_logging(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s'))
        logger.addHandler(sh)
    return logger

def ensure_folders(base_dir):
    for folder in ["LOGID", "TULEMUSED"]:
        os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

def get_local_subnet():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ".".join(ip.split(".")[:-1]) + ".0/24"
    except:
        return "127.0.0.1/24"
