"""Independently validate font.agnb against font metadata and glyph payloads."""

import sqlite3
from pathlib import Path

from validate_ui_agnb import read_image_records


def validate_font_agnb(db_path, container_path, rgba_dir):
    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute(
            """
            SELECT char_num, dim_x, dim_y, img_filename
            FROM tbl_91a_font
            WHERE font_name = 'itc_honda'
            ORDER BY char_num
            """
        ).fetchall()
    finally:
        conn.close()

    expected = [
        (
            0x1100 + char_num,
            width,
            height,
            (Path(rgba_dir) / Path(filename).with_suffix(".rgba2")).read_bytes(),
        )
        for char_num, width, height, filename in rows
    ]
    actual = read_image_records(container_path)
    if actual != expected:
        raise ValueError("font container differs from metadata or glyph payloads")
    print(f"Validated {len(actual)} font records byte-for-byte in {container_path}")


if __name__ == "__main__":
    validate_font_agnb(
        "build/data/build.db",
        "tgt/font.agnb",
        "build/fonts/honda/rgba2",
    )
