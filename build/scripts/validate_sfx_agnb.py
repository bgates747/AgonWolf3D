"""Independently validate sfx.agnb against the SFX catalog and PCM WAVs."""

import sqlite3
import struct
import wave
from pathlib import Path

from validate_ui_agnb import _chunk


def validate_sfx_agnb(db_path, container_path, wav_dir):
    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute(
            """
            SELECT sfx_id, size, sample_rate, filename
            FROM tbl_08_sfx
            ORDER BY sfx_id
            """
        ).fetchall()
    finally:
        conn.close()

    expected = []
    for sfx_id, size, sample_rate, filename in rows:
        with wave.open(str(Path(wav_dir) / filename), "rb") as wav:
            pcm = wav.readframes(wav.getnframes())
        if len(pcm) != size:
            raise ValueError(f"PCM size mismatch for {filename}")
        expected.append((0xFB00 + sfx_id, 0x09, sample_rate, pcm))

    data = Path(container_path).read_bytes()
    if data[:4] != b"RIFF" or data[8:12] != b"AGNB":
        raise ValueError("invalid RIFF/AGNB header")
    if struct.unpack_from("<I", data, 4)[0] != len(data) - 8:
        raise ValueError("RIFF size does not match physical file size")

    offset = 12
    chunk_id, payload, offset = _chunk(data, offset, len(data))
    if chunk_id != b"VERS" or payload != b"\x00\x02":
        raise ValueError("expected AGNB version 0.2")

    actual = []
    while offset < len(data):
        chunk_id, payload, offset = _chunk(data, offset, len(data))
        if chunk_id != b"LIST" or payload[:4] != b"BUFR":
            raise ValueError("expected LIST BUFR record")
        nested_offset = 4
        nested = []
        while nested_offset < len(payload):
            item_id, item_payload, nested_offset = _chunk(
                payload, nested_offset, len(payload)
            )
            nested.append((item_id, item_payload))
        if [item[0] for item in nested] != [b"BHDR", b"AUDI", b"DATA"]:
            raise ValueError("unexpected audio record chunk sequence")
        buffer_id = struct.unpack("<H", nested[0][1])[0]
        audio_format, sample_rate = struct.unpack("<BH", nested[1][1])
        actual.append((buffer_id, audio_format, sample_rate, nested[2][1]))

    if actual != expected:
        raise ValueError("audio container differs from catalog or PCM inputs")
    print(f"Validated {len(actual)} audio records byte-for-byte in {container_path}")


if __name__ == "__main__":
    validate_sfx_agnb(
        "build/data/build.db",
        "tgt/sfx.agnb",
        "build/sfx/wav",
    )
