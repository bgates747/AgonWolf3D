"""Build the UI image AGNB container with the application's established IDs."""

import sqlite3
from pathlib import Path

from build_05a_make_images_agnb import ImageRecord, build_container


def _records(db_path, table, rgba_dir, first_buffer_id, family):
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

    records = []
    for index, (name, width, height) in enumerate(rows):
        rgba_file = Path(rgba_dir) / f"{name}.rgba2"
        data_size = rgba_file.stat().st_size
        expected_size = width * height
        if data_size != expected_size:
            raise ValueError(
                f"{family} payload size mismatch for {name}: "
                f"expected {expected_size}, found {data_size}"
            )
        records.append(
            ImageRecord(
                name=f"{family}/{name}",
                buffer_id=first_buffer_id + index,
                width=width,
                height=height,
                rgba_file=rgba_file,
                data_size=data_size,
            )
        )
    return records


def make_ui_agnb(db_path, core_rgba_dir, bj_rgba_dir, output_path):
    records = (
        _records(db_path, "tbl_91b_UI", core_rgba_dir, 0x2000, "ui")
        + _records(db_path, "tbl_91c_UI_BJ", bj_rgba_dir, 0x2100, "bj")
    )
    if not records:
        raise ValueError("The UI image catalog is empty")

    buffer_ids = [record.buffer_id for record in records]
    if len(buffer_ids) != len(set(buffer_ids)):
        raise ValueError("Duplicate UI buffer ID")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    container = build_container(records)
    output_path.write_bytes(container)
    print(
        f"Generated {output_path} with {len(records)} UI image records "
        f"({len(container)} bytes)"
    )
    return records


if __name__ == "__main__":
    make_ui_agnb(
        "build/data/build.db",
        "build/ui/rgba2/core",
        "build/ui/rgba2/bj",
        "tgt/ui.agnb",
    )
