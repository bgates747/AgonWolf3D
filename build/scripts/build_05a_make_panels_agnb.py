"""Build the panels-only AGNB image container.

The RIFF/AGNB writer is adapted from the hardware-proven implementation in:

    agon-utils/examples/agnb/container/scripts/do_assembly.py

The panel catalog and ordering are shared with build_91_asm_images.py so the
container's explicit buffer IDs remain identical to the generated BUF_* values.
"""

import struct
from dataclasses import dataclass
from pathlib import Path

from build_91_asm_images import get_panels_data


VERSION_MAJOR = 0
VERSION_MINOR = 1
IMAGE_FORMAT_RGBA2222 = 1
FIRST_PANEL_BUFFER_ID = 0x0100
MAX_U16 = 0xFFFF
MAX_U32 = 0xFFFFFFFF


@dataclass(frozen=True)
class ImageRecord:
    """Validated inputs for one LIST BUFR image record."""

    name: str
    buffer_id: int
    width: int
    height: int
    rgba_file: Path
    data_size: int


def align4(size):
    return (size + 3) & ~3


def make_chunk(chunk_id, payload):
    """Return one aligned RIFF chunk, including its header and zero padding."""
    if len(chunk_id) != 4:
        raise ValueError(f"RIFF chunk ID must contain four bytes: {chunk_id!r}")
    if len(payload) > MAX_U32:
        raise ValueError(f"RIFF payload is too large: {len(payload)} bytes")

    padding = bytes(align4(len(payload)) - len(payload))
    return chunk_id + struct.pack("<I", len(payload)) + payload + padding


def load_panel_records(db_path, panels_rgba_dir):
    """Build and validate the ordered cube/panel catalog."""
    panels_rgba_dir = Path(panels_rgba_dir)
    rows = get_panels_data(db_path, "cube")
    records = []
    names = set()
    buffer_ids = set()

    for index, row in enumerate(rows):
        name = row["panel_base_filename"]
        buffer_id = FIRST_PANEL_BUFFER_ID + index
        width = row["dim_x"]
        height = row["dim_y"]
        rgba_file = panels_rgba_dir / f"{name}.rgba2"

        if name in names:
            raise ValueError(f"Duplicate panel name: {name}")
        if buffer_id in buffer_ids:
            raise ValueError(f"Duplicate panel buffer ID: 0x{buffer_id:04X}")
        if buffer_id >= MAX_U16:
            raise ValueError(f"Invalid panel buffer ID: 0x{buffer_id:04X}")
        if not 0 < width <= MAX_U16 or not 0 < height <= MAX_U16:
            raise ValueError(f"Invalid dimensions for {name}: {width}x{height}")
        if not rgba_file.is_file():
            raise FileNotFoundError(f"Missing panel payload: {rgba_file}")

        data_size = rgba_file.stat().st_size
        expected_size = width * height
        if data_size != expected_size:
            raise ValueError(
                f"RGBA2222 size mismatch for {name}: "
                f"expected {expected_size}, found {data_size}"
            )

        names.add(name)
        buffer_ids.add(buffer_id)
        records.append(
            ImageRecord(
                name=name,
                buffer_id=buffer_id,
                width=width,
                height=height,
                rgba_file=rgba_file,
                data_size=data_size,
            )
        )

    if not records:
        raise ValueError("The panel catalog is empty")
    return records


def make_buffer_record(record):
    """Return one aligned LIST BUFR record."""
    pixels = record.rgba_file.read_bytes()
    if len(pixels) != record.data_size:
        raise RuntimeError(
            f"RGBA2222 file changed while building: {record.rgba_file}"
        )

    nested_chunks = b"".join(
        (
            make_chunk(b"BHDR", struct.pack("<H", record.buffer_id)),
            make_chunk(
                b"IMAG",
                struct.pack(
                    "<HHB",
                    record.width,
                    record.height,
                    IMAGE_FORMAT_RGBA2222,
                ),
            ),
            make_chunk(b"DATA", pixels),
        )
    )
    return make_chunk(b"LIST", b"BUFR" + nested_chunks)


def build_container(records):
    """Compile validated image records into one complete RIFF AGNB file."""
    if not records:
        raise ValueError("An AGNB container requires at least one buffer record")

    body = bytearray(b"AGNB")
    body.extend(make_chunk(b"VERS", bytes((VERSION_MAJOR, VERSION_MINOR))))
    for record in records:
        body.extend(make_buffer_record(record))

    if len(body) > MAX_U32:
        raise ValueError(f"RIFF container is too large: {len(body) + 8} bytes")
    return b"RIFF" + struct.pack("<I", len(body)) + body


def remove_containerized_panel_files(records):
    """Remove cube payload intermediates after the container is complete."""
    for record in records:
        record.rgba_file.unlink()
    print(f"Removed {len(records)} containerized panel intermediates")


def make_panels_agnb(db_path, panels_rgba_dir, output_path):
    records = load_panel_records(db_path, panels_rgba_dir)
    container = build_container(records)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(container)
    print(
        f"Generated {output_path} with {len(records)} panel records "
        f"({len(container)} bytes)"
    )
    remove_containerized_panel_files(records)
    return records


if __name__ == "__main__":
    make_panels_agnb(
        "build/data/build.db",
        "tgt/panels",
        "tgt/images.agnb",
    )
