"""Build the ITC Honda proportional-glyph AGNB image container."""

import sqlite3
from pathlib import Path

from build_05a_make_images_agnb import ImageRecord, build_container


def load_font_records(db_path, rgba_dir, font_name="itc_honda"):
    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute(
            """
            SELECT char_num, dim_x, dim_y, img_filename
            FROM tbl_91a_font
            WHERE font_name = ?
            ORDER BY char_num
            """,
            (font_name,),
        ).fetchall()
    finally:
        conn.close()

    records = []
    for char_num, width, height, img_filename in rows:
        rgba_file = Path(rgba_dir) / Path(img_filename).with_suffix(".rgba2")
        data_size = rgba_file.stat().st_size
        expected_size = width * height
        if data_size != expected_size:
            raise ValueError(
                f"Glyph {char_num} payload mismatch: expected "
                f"{expected_size}, found {data_size}"
            )
        records.append(
            ImageRecord(
                name=f"{font_name}/{char_num:03d}",
                buffer_id=0x1100 + char_num,
                width=width,
                height=height,
                rgba_file=rgba_file,
                data_size=data_size,
            )
        )
    if not records:
        raise ValueError(f"No glyphs found for {font_name}")
    return records


def make_font_agnb(db_path, rgba_dir, output_path):
    records = load_font_records(db_path, rgba_dir)
    container = build_container(records)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(container)
    print(
        f"Generated {output_path} with {len(records)} font image records "
        f"({len(container)} bytes)"
    )
    return records


if __name__ == "__main__":
    make_font_agnb(
        "build/data/build.db",
        "build/fonts/honda/rgba2",
        "tgt/font.agnb",
    )
