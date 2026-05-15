#!/usr/bin/env python3
"""
VALVUR - Automaattestid
Käivitus: python3 -m pytest tests/test_skriptid.py
"""

import os
import sys
import tempfile
import unittest
import importlib.util

TEST_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKRIPT_DIR = os.path.join(TEST_DIR, "SKRIPT_2")
sys.path.insert(0, SKRIPT_DIR)

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SKRIPT_DIR, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

class TestUtils(unittest.TestCase):
    def test_get_output_dir_default(self):
        import utils
        if "VALVUR_OUT" in os.environ:
            del os.environ["VALVUR_OUT"]
        out_dir = utils.get_output_dir()
        self.assertTrue(out_dir.endswith("TULEMUSED"))

    def test_get_output_dir_env(self):
        import utils
        os.environ["VALVUR_OUT"] = "/tmp/valvur_test"
        out_dir = utils.get_output_dir()
        self.assertEqual(out_dir, "/tmp/valvur_test")
        del os.environ["VALVUR_OUT"]

    def test_setup_logging(self):
        import utils
        logger = utils.setup_logging("TEST")
        self.assertEqual(logger.name, "TEST")

    def test_get_local_subnet(self):
        import utils
        subnet = utils.get_local_subnet()
        self.assertTrue(subnet.endswith("/24"))

    def test_ensure_folders(self):
        import utils
        with tempfile.TemporaryDirectory() as tmpdir:
            utils.ensure_folders(tmpdir)
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "LOGID")))
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "TULEMUSED")))

    def test_valvur_event_to_dict(self):
        import utils
        event = utils.ValvurEvent("2025-01-01", "Security", 4625, "High", "Test", "T1110")
        d = event.to_dict()
        self.assertEqual(d["Aeg"], "2025-01-01")
        self.assertEqual(d["MITRE"], "T1110")

class TestTerviklus(unittest.TestCase):
    def test_calculate_sha256(self):
        tvk = load_module("terviklus", "00_terviklus_kontroll.py")
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b"test andmed")
            f.flush()
            fname = f.name
        try:
            h = tvk.calculate_sha256(fname)
            self.assertEqual(len(h), 64)
        finally:
            os.unlink(fname)

class TestFuzzyMatch(unittest.TestCase):
    def test_fuzzy_match(self):
        omj = load_module("marksonad", "04_otsing_marksonade_jargi.py")
        r = omj.fuzzy_match("mimikatz", "mimikatz")
        self.assertAlmostEqual(r, 1.0)
        r2 = omj.fuzzy_match("hello", "world")
        self.assertLess(r2, 0.5)

class TestXOR(unittest.TestCase):
    def test_xor_decrypt(self):
        psd = load_module("psdecode", "05_powershell_dekodeerimine.py")
        data = bytearray([0x48, 0x65, 0x6c, 0x6c, 0x6f])
        enc = psd.xor_decrypt(data, 0x01)
        dec = psd.xor_decrypt(enc, 0x01)
        self.assertEqual(dec, data)

class TestLinuxLogid(unittest.TestCase):
    def test_parse_no_logs(self):
        import utils
        llc = load_module("linuxlog", "02_linux_logid_csv.py")
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["VALVUR_OUT"] = tmpdir
            result = llc.parse_linux_logs()
            self.assertIsNone(result)
            del os.environ["VALVUR_OUT"]

class TestThreatIntel(unittest.TestCase):
    def test_extract_ips(self):
        ti = load_module("threatintel", "10_threat_intel.py")
        ips = ti.extract_ips("Siin on IP 192.168.1.1 ja 10.0.0.1")
        self.assertIn("192.168.1.1", ips)
        self.assertIn("10.0.0.1", ips)

    def test_extract_ips_empty(self):
        ti = load_module("threatintel", "10_threat_intel.py")
        ips = ti.extract_ips("Siin pole IP aadresse")
        self.assertEqual(len(ips), 0)

class TestKahtlasedFailid(unittest.TestCase):
    def test_live_scan_linux(self):
        kf = load_module("kahtlased", "06_kahtlased_failid.py")
        import platform
        if platform.system() != "Windows":
            results = kf.live_system_scan()
            self.assertIsInstance(results, list)

class TestRaport(unittest.TestCase):
    def test_count_csv_rows_empty(self):
        gr = load_module("genereeriraport", "14_genereeriRAPORT.py")
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("header1,header2\n")
            fname = f.name
        try:
            count = gr.count_csv_rows(fname)
            self.assertEqual(count, 0)
        finally:
            os.unlink(fname)

if __name__ == "__main__":
    unittest.main()
