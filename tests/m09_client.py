"""Finite local client packaging checks; editor/Node observations are separate."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class LocalClientPackage(unittest.TestCase):
    def test_deterministic_closed_source_payload_and_manifest(self):
        source = ROOT / "editors/vscode/package_vsix.py"
        spec = importlib.util.spec_from_file_location("local_client_packager", source)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            first, second = Path(tmp) / "first.vsix", Path(tmp) / "second.vsix"
            module.package(first); module.package(second)
            self.assertEqual(hashlib.sha256(first.read_bytes()).digest(), hashlib.sha256(second.read_bytes()).digest())
            with zipfile.ZipFile(first) as archive:
                self.assertEqual(set(archive.namelist()), {"extension/" + name for name in module.PAYLOAD} | {"extension.vsixmanifest", "[Content_Types].xml"})
                for name in module.PAYLOAD:
                    self.assertEqual(archive.read("extension/" + name), (source.parent / name).read_bytes())
                metadata = json.loads(archive.read("extension/package.json"))
                self.assertNotIn("dependencies", metadata)
                self.assertFalse(metadata["capabilities"]["untrustedWorkspaces"]["supported"])
                self.assertEqual(metadata["main"], "./extension.js")
                self.assertEqual(ET.fromstring(archive.read("extension.vsixmanifest")).attrib["Version"], "2.0.0")
                ET.fromstring(archive.read("[Content_Types].xml"))
            with self.assertRaises(FileExistsError): module.package(first)


if __name__ == "__main__": unittest.main()
