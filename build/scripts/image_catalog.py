"""Shared build-time image catalog and buffer-ID assignments."""

from dataclasses import dataclass
from pathlib import Path
import sqlite3
import struct


FIRST_IMAGE_BUFFER_ID = 0x0100
INVALID_BUFFER_ID = 0xFFFF


@dataclass(frozen=True)
class ImageCatalogEntry:
    family: str
    name: str
    buffer_id: int
    width: int
    height: int
    payload_path: Path


def dict_factory(cursor, row):
    return {
        description[0]: row[index]
        for index, description in enumerate(cursor.description)
    }


def get_panels_data(db_path, render_type):
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = dict_factory
        return conn.execute(
            """
            select distinct panel_base_filename, dim_x, dim_y
            from tbl_04_panels_lookup
            where render_type = ?
            order by panel_base_filename;
            """,
            (render_type,),
        ).fetchall()


def get_dws_data(db_path):
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = dict_factory
        return conn.execute(
            """
            select panel_base_filename, dim_x, dim_y
            from tbl_04a_dws_lookup
            order by distance;
            """
        ).fetchall()


def build_image_catalog(
    db_path,
    cube_rgba_dir="build/panels/rgba2",
    sprite_rgba_dir="tgt/panels",
    dws_rgba_dir="tgt/dws",
):
    """Assign deterministic IDs to every active world-image family."""
    sources = (
        ("cube", get_panels_data(db_path, "cube"), Path(cube_rgba_dir)),
        ("sprite", get_panels_data(db_path, "sprite"), Path(sprite_rgba_dir)),
        ("dws", get_dws_data(db_path), Path(dws_rgba_dir)),
    )
    catalog = []
    names = set()
    assembly_names = set()

    for family, rows, payload_dir in sources:
        for row in rows:
            buffer_id = FIRST_IMAGE_BUFFER_ID + len(catalog)
            name = row["panel_base_filename"]
            assembly_name = name.upper()
            width = row["dim_x"]
            height = row["dim_y"]
            if name in names:
                raise ValueError(f"Duplicate image catalog name: {name}")
            if assembly_name in assembly_names:
                raise ValueError(
                    f"Duplicate assembly image symbol after uppercasing: {name}"
                )
            if buffer_id >= INVALID_BUFFER_ID:
                raise ValueError(f"Invalid image buffer ID: 0x{buffer_id:04X}")
            if not 0 < width <= 0xFFFF or not 0 < height <= 0xFFFF:
                raise ValueError(
                    f"Invalid image dimensions for {name}: {width}x{height}"
                )
            catalog.append(
                ImageCatalogEntry(
                    family=family,
                    name=name,
                    buffer_id=buffer_id,
                    width=width,
                    height=height,
                    payload_path=payload_dir / f"{name}.rgba2",
                )
            )
            names.add(name)
            assembly_names.add(assembly_name)

    if not catalog:
        raise ValueError("The image catalog is empty")
    return catalog


def family_entries(catalog, family):
    return [entry for entry in catalog if entry.family == family]


def read_agnb_buffer_ids(path):
    """Read ordered BHDR IDs from a strict-layout AGNB 0.1 container."""
    data = Path(path).read_bytes()
    if len(data) < 12 or data[:4] != b"RIFF" or data[8:12] != b"AGNB":
        raise ValueError(f"Invalid RIFF AGNB header: {path}")
    if struct.unpack_from("<I", data, 4)[0] + 8 != len(data):
        raise ValueError(f"Invalid RIFF size: {path}")

    ids = []
    offset = 12
    while offset < len(data):
        chunk_id = data[offset : offset + 4]
        chunk_size = struct.unpack_from("<I", data, offset + 4)[0]
        payload = offset + 8
        chunk_end = payload + ((chunk_size + 3) & ~3)
        if chunk_end > len(data):
            raise ValueError(f"AGNB chunk exceeds container bounds: {path}")

        if chunk_id == b"VERS":
            offset = chunk_end
            continue
        if chunk_id != b"LIST" or data[payload : payload + 4] != b"BUFR":
            raise ValueError(f"Unexpected AGNB top-level chunk: {chunk_id!r}")

        bhdr = payload + 4
        if data[bhdr : bhdr + 4] != b"BHDR":
            raise ValueError(f"AGNB BUFR record does not begin with BHDR: {path}")
        if struct.unpack_from("<I", data, bhdr + 4)[0] != 2:
            raise ValueError(f"Invalid AGNB BHDR size: {path}")
        ids.append(struct.unpack_from("<H", data, bhdr + 8)[0])
        offset = chunk_end

    return ids


def assert_cube_ids_match_agnb(catalog, path):
    expected = [entry.buffer_id for entry in family_entries(catalog, "cube")]
    actual = read_agnb_buffer_ids(path)
    if actual != expected:
        raise RuntimeError(
            "AGNB cube buffer IDs do not match the shared image catalog: "
            f"expected {expected}, found {actual}"
        )
    print(f"Validated {len(actual)} AGNB buffer IDs against the shared catalog")
