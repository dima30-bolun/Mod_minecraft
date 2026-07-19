#!/usr/bin/env python3
"""Build Echoes of the Nexus distributable files without storing binaries in git.

The repository intentionally tracks only text/source files. This script generates
minimal PNG item textures, a silent WAV used by sound definitions, the installable
.mcaddon archive, and a full source ZIP in dist/.
"""
from __future__ import annotations

import struct
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BP = ROOT / "EchosOfTheNexus_BP"
RP = ROOT / "EchosOfTheNexus_RP"
DIST = ROOT / "dist"
WORLDS = [
    "emberglass",
    "mossveil",
    "tideclock",
    "skyforge",
    "umbra",
    "frostloom",
    "brasshollow",
    "starfall",
    "mirrordune",
    "nexus",
]
TEXT_SOURCE_FILES = ["README.md", "LICENSE", "CHANGELOG.md", "STORY_BIBLE.md"]


def png_rgba(color: tuple[int, int, int, int]) -> bytes:
    width = height = 16
    raw = b"".join(b"\x00" + bytes(color) * width for _ in range(height))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + kind
            + data
            + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        )

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


def silent_wav() -> bytes:
    return (
        b"RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00"
        b"@\x1f\x00\x00@\x1f\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00"
    )


def generate_assets() -> None:
    item_dir = RP / "textures" / "items"
    music_dir = RP / "sounds" / "music"
    item_dir.mkdir(parents=True, exist_ok=True)
    music_dir.mkdir(parents=True, exist_ok=True)
    for index, world_id in enumerate(WORLDS):
        color = ((50 + index * 20) % 255, (80 + index * 31) % 255, (160 + index * 13) % 255, 255)
        (item_dir / f"{world_id}_blade.png").write_bytes(png_rgba(color))
    (music_dir / "silence.wav").write_bytes(silent_wav())


def write_zip(output: Path, inputs: list[Path]) -> None:
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in inputs:
            if path.is_dir():
                for file_path in sorted(path.rglob("*")):
                    if file_path.is_file():
                        archive.write(file_path, file_path.relative_to(ROOT))
            elif path.exists():
                archive.write(path, path.relative_to(ROOT))


def build() -> None:
    DIST.mkdir(exist_ok=True)
    generate_assets()
    write_zip(DIST / "EchoesOfTheNexus.mcaddon", [BP, RP])
    write_zip(DIST / "EchoesOfTheNexus_source.zip", [BP, RP, *[ROOT / name for name in TEXT_SOURCE_FILES]])
    print("Built dist/EchoesOfTheNexus.mcaddon")
    print("Built dist/EchoesOfTheNexus_source.zip")


if __name__ == "__main__":
    build()
