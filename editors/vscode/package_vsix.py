"""Closed local VSIX payload; no dependency install or Marketplace publication."""
import argparse
import json
from pathlib import Path
import zipfile
from xml.sax.saxutils import escape

PAYLOAD = ("package.json", "extension.js", "transport.js", "README.md")


def package(output):
    root = Path(__file__).resolve().parent
    metadata = json.loads((root / "package.json").read_text())
    identity = {key: escape(metadata[key], {'"': '&quot;'}) for key in ("name", "publisher", "version", "displayName", "description")}
    manifest = '''<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011">
<Metadata><Identity Language="en-US" Id="{name}" Version="{version}" Publisher="{publisher}"/><DisplayName>{displayName}</DisplayName><Description xml:space="preserve">{description}</Description><Tags>python</Tags><Categories>Programming Languages</Categories><Properties><Property Id="Microsoft.VisualStudio.Code.Engine" Value="^1.139.0"/><Property Id="Microsoft.VisualStudio.Code.ExtensionKind" Value="workspace"/></Properties></Metadata>
<Installation><InstallationTarget Id="Microsoft.VisualStudio.Code"/></Installation><Dependencies/><Assets><Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true"/></Assets>
</PackageManifest>'''.format(**identity)
    content_types = '''<?xml version="1.0" encoding="utf-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="json" ContentType="application/json"/><Default Extension="js" ContentType="application/javascript"/><Default Extension="md" ContentType="text/plain"/><Default Extension="vsixmanifest" ContentType="text/xml"/></Types>'''
    entries = {"extension/" + name: (root / name).read_bytes() for name in PAYLOAD}
    entries.update({"extension.vsixmanifest": manifest.encode(), "[Content_Types].xml": content_types.encode()})
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, raw in sorted(entries.items()):
            entry = zipfile.ZipInfo(name, (2026, 10, 9, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, raw)
    return list(entries)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    package(Path(args.output))
