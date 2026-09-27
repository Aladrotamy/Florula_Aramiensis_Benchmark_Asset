"""Write MANIFEST.sha256: a checksum for every file tracked by git.

Usage (from the asset root, after committing):
    python tools/make_manifest.py

Text files are hashed after normalising CRLF to LF, so the manifest matches a
fresh clone on any operating system. PDF and image files are hashed as bytes.
"""
import hashlib, subprocess

BINARY = (".pdf", ".png", ".jpg")
files = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout.split("\n")
lines = []
for f in sorted(x for x in files if x and x != "MANIFEST.sha256"):
    b = open(f, "rb").read()
    if not f.lower().endswith(BINARY):
        b = b.replace(b"\r\n", b"\n")
    lines.append(f"{hashlib.sha256(b).hexdigest()}  {f}")
with open("MANIFEST.sha256", "w", encoding="utf-8", newline="\n") as out:
    out.write("\n".join(lines) + "\n")
print(f"MANIFEST.sha256: {len(lines)} files")
