"""Build the AGNB 0.2 sound-effect container from processed PCM WAV files."""

import sqlite3
import struct
import wave
from pathlib import Path

from build_05a_make_images_agnb import make_chunk


def make_sfx_agnb(db_path, wav_dir, output_path, first_buffer_id=0xFB00):
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

    body = bytearray(b"AGNB")
    body.extend(make_chunk(b"VERS", bytes((0, 2))))
    for sfx_id, expected_size, expected_rate, filename in rows:
        wav_path = Path(wav_dir) / filename
        with wave.open(str(wav_path), "rb") as wav:
            if wav.getcomptype() != "NONE":
                raise ValueError(f"{filename} is not uncompressed PCM")
            if wav.getnchannels() != 1 or wav.getsampwidth() != 1:
                raise ValueError(f"{filename} must be unsigned 8-bit mono PCM")
            sample_rate = wav.getframerate()
            pcm = wav.readframes(wav.getnframes())
        if len(pcm) != expected_size or sample_rate != expected_rate:
            raise ValueError(f"Database metadata differs from {filename}")

        buffer_id = first_buffer_id + sfx_id
        nested = b"".join(
            (
                make_chunk(b"BHDR", struct.pack("<H", buffer_id)),
                make_chunk(b"AUDI", struct.pack("<BH", 0x09, sample_rate)),
                make_chunk(b"DATA", pcm),
            )
        )
        body.extend(make_chunk(b"LIST", b"BUFR" + nested))

    if not rows:
        raise ValueError("The sound-effect catalog is empty")
    container = b"RIFF" + struct.pack("<I", len(body)) + body
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(container)
    print(
        f"Generated {output_path} with {len(rows)} audio records "
        f"({len(container)} bytes)"
    )


if __name__ == "__main__":
    make_sfx_agnb(
        "build/data/build.db",
        "build/sfx/wav",
        "tgt/sfx.agnb",
    )
