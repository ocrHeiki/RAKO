#!/usr/bin/env python3
import os
import sys
import logging
import platform
import subprocess
import socket
from datetime import datetime

# Ühtne andmemudel (Punkt 1)
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

def setup_logging(name):
    """Seadistab standardse logging mooduli (Punkt 5)."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
    
    # Konsooli väljund
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    
    return logger

def ensure_folders(base_dir):
    """Loob vajalikud kaustad automaatselt (Punkt 2)."""
    for folder in ["LOGID", "TULEMUSED", "SKRIPTID"]:
        path = os.path.join(base_dir, folder)
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

def get_local_subnet():
    """Tuvastab kohaliku alamvõrgu (Windows & Linux tugi - Punkt 2)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ".".join(ip.split(".")[:-1]) + ".0/24"
    except:
        return "127.0.0.1/24"

def is_admin():
    """Süsteemne privileegide kontroll."""
    if platform.system() == "Windows":
        import ctypes
        try: return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except: return False
    return os.getuid() == 0
