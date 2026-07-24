"""Independently validate ui.agnb against its generated RGBA2222 inputs."""

import sqlite3
import struct
from pathlib import Path


def _chunk(data, offset, limit):
    if offset + 8 > limit:
        raise ValueError("truncated chunk header")
    chunk_id = data[offset : offset + 4]
    size = struct.unpack_from("<I", data, offset + 4)[0]
    start = offset + 8
    end = start + size
    next_offset = start + ((size + 3) & ~3)
    if end > limit or next_offset > limit:
        raise ValueError(f"{chunk_id!r} exceeds its enclosing chunk")
    if any(data[end:next_offset]):
        raise ValueError(f"{chunk_id!r} has nonzero alignment padding")
    return chunk_id, data[start:end], next_offset


def _expected(db_path, table, rgba_dir, first_id):
    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute(
            f"""
            SELECT panel_base_filename, dim_x, dim_y
            FROM {table}
            ORDER BY panel_base_filename
            """
        ).fetchall()
    finally:
        conn.close()
    return [
        (first_id + index, width, height, (Path(rgba_dir) / f"{name}.rgba2").read_bytes())
        for index, (name, width, height) in enumerate(rows)
    ]


def validate_ui_agnb(db_path, container_path, core_rgba_dir, bj_rgba_dir):
    expected = (
        _expected(db_path, "tbl_91b_UI", core_rgba_dir, 0x2000)
        + _expected(db_path, "tbl_91c_UI_BJ", bj_rgba_dir, 0x2100)
    )
    actual = read_image_records(container_path)
    if actual != expected:
        raise ValueError("container records differ from catalog or payload inputs")
    print(f"Validated {len(actual)} UI records byte-for-byte in {container_path}")


def read_image_records(container_path):
    data = Path(container_path).read_bytes()
    if data[:4] != b"RIFF" or data[8:12] != b"AGNB":
        raise ValueError("invalid RIFF/AGNB header")
    if struct.unpack_from("<I", data, 4)[0] != len(data) - 8:
        raise ValueError("RIFF size does not match physical file size")

    offset = 12
    chunk_id, payload, offset = _chunk(data, offset, len(data))
    if chunk_id != b"VERS" or payload != b"\x00\x01":
        raise ValueError("expected AGNB version 0.1")

    actual = []
    while offset < len(data):
        chunk_id, payload, offset = _chunk(data, offset, len(data))
        if chunk_id != b"LIST" or payload[:4] != b"BUFR":
            raise ValueError("expected LIST BUFR record")
        nested_offset = 4
        nested = []
        while nested_offset < len(payload):
            sub_id, sub_payload, nested_offset = _chunk(
                payload, nested_offset, len(payload)
            )
            nested.append((sub_id, sub_payload))
        if [item[0] for item in nested] != [b"BHDR", b"IMAG", b"DATA"]:
            raise ValueError("unexpected LIST BUFR chunk sequence")
        buffer_id = struct.unpack("<H", nested[0][1])[0]
        width, height, image_format = struct.unpack("<HHB", nested[1][1])
        if image_format != 1:
            raise ValueError(f"buffer 0x{buffer_id:04X} is not RGBA2222")
        actual.append((buffer_id, width, height, nested[2][1]))

    return actual


if __name__ == "__main__":
    validate_ui_agnb(
        "build/data/build.db",
        "tgt/ui.agnb",
        "build/ui/rgba2/core",
        "build/ui/rgba2/bj",
    )
