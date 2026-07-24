from image_catalog import (
    assert_cube_ids_match_agnb,
    build_image_catalog,
    family_entries,
    get_dws_data,
    get_panels_data,
)


# Generate image buffer constants and lookup tables. Cube/panel payloads are
# deployed through images.agnb; sprites and distance walls retain loose-file
# loaders during the first container integration phase.
def write_asm_image_family(
    panels_inc_path,
    render_type,
    src_img_dir,
    entries,
    emit_loose_file_loaders=True,
):
    with open(panels_inc_path, "a") as asm_writer:
        asm_writer.write(f"\n; {render_type} buffer ids:\n")
        for entry in entries:
            asm_writer.write(
                f"BUF_{entry.name.upper()}: equ 0x{entry.buffer_id:04X}\n"
            )

        asm_writer.write(f"\n{render_type}_num_panels: equ {len(entries)} \n")

        asm_writer.write(f"\n; {render_type} buffer id reverse lookup:\n")
        asm_writer.write(f"{render_type}_buffer_id_lut:\n")
        for entry in entries:
            asm_writer.write(f"\tdl BUF_{entry.name.upper()}\n")

        if not emit_loose_file_loaders:
            return

        asm_writer.write(f"\n; {render_type} load routines jump table:\n")
        asm_writer.write(f"{render_type}_load_panels_table:\n")
        for entry in entries:
            asm_writer.write(f"\tdl ld_{entry.name}\n")

        asm_writer.write(
            f"\n; Import {render_type} .rgba2 bitmap files and load them into "
            "VDP buffers\n"
        )
        for entry in entries:
            const_name = f"BUF_{entry.name.upper()}"
            asm_writer.write("\n")
            asm_writer.write(f"ld_{entry.name}:\n")
            asm_writer.write(f"\tld hl,F{entry.name}\n")
            asm_writer.write("\tld (cur_filename),hl\n")
            asm_writer.write("\tld de,filedata\n")
            asm_writer.write("\tld bc,65536\n")
            asm_writer.write("\tld a,mos_load\n")
            asm_writer.write("\tRST.LIL 08h\n")
            asm_writer.write(f"\tld hl,{const_name}\n")
            asm_writer.write(f"\tld bc,{entry.width}\n")
            asm_writer.write(f"\tld de,{entry.height}\n")
            asm_writer.write(f"\tld ix,{entry.width * entry.height}\n")
            asm_writer.write("\tcall vdu_load_img\n")
            asm_writer.write("\tret\n")

        asm_writer.write("\n; File name lookups:\n")
        for entry in entries:
            asm_writer.write(
                f'F{entry.name}: db "{src_img_dir}/{entry.name}.rgba2",0\n'
            )


def make_asm_images_inc(
    db_path,
    panels_inc_path,
    agnb_path="tgt/images.agnb",
):
    catalog = build_image_catalog(db_path)
    with open(panels_inc_path, "w") as asm_writer:
        asm_writer.write(
            "; This file is created by build_91_asm_images.py, do not edit it!\n"
        )

    write_asm_image_family(
        panels_inc_path,
        "cube",
        "panels",
        family_entries(catalog, "cube"),
        emit_loose_file_loaders=False,
    )
    write_asm_image_family(
        panels_inc_path,
        "sprite",
        "panels",
        family_entries(catalog, "sprite"),
    )
    write_asm_image_family(
        panels_inc_path,
        "dws",
        "dws",
        family_entries(catalog, "dws"),
    )

    assert_cube_ids_match_agnb(catalog, agnb_path)
    return catalog


if __name__ == "__main__":
    make_asm_images_inc(
        "build/data/build.db",
        "src/asm/images.asm",
        "tgt/images.agnb",
    )
