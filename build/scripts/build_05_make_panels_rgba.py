import shutil
from pathlib import Path

import PIL as pillow
from agonImages import img_to_rgba2

from image_catalog import get_panels_data


def catalog_names(db_path, render_type):
    return {
        row["panel_base_filename"]
        for row in get_panels_data(db_path, render_type)
    }


def recreate_directory(path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def make_panels_rgba(
    db_path,
    panels_png_dir,
    cube_rgba_dir,
    sprite_rgba_dir,
):
    """Convert transformed PNGs, separating build-only cubes from sprites."""
    panels_png_dir = Path(panels_png_dir)
    cube_rgba_dir = Path(cube_rgba_dir)
    sprite_rgba_dir = Path(sprite_rgba_dir)
    cube_names = catalog_names(db_path, "cube")
    sprite_names = catalog_names(db_path, "sprite")

    overlap = cube_names & sprite_names
    if overlap:
        names = ", ".join(sorted(overlap))
        raise ValueError(f"Cube and sprite output names overlap: {names}")

    recreate_directory(cube_rgba_dir)
    recreate_directory(sprite_rgba_dir)

    converted = {"cube": 0, "sprite": 0}
    for png_path in sorted(panels_png_dir.glob("*.png")):
        name = png_path.stem
        if name in cube_names:
            output_dir = cube_rgba_dir
            family = "cube"
        elif name in sprite_names:
            output_dir = sprite_rgba_dir
            family = "sprite"
        else:
            raise ValueError(f"Uncatalogued transformed panel image: {png_path}")

        # Palette conversion has already occurred upstream when Mapmaker
        # textures are imported by build_02_fetch_tiles.py.
        with pillow.Image.open(png_path) as img:
            img_to_rgba2(img, output_dir / f"{name}.rgba2")
        converted[family] += 1

    expected = {"cube": len(cube_names), "sprite": len(sprite_names)}
    if converted != expected:
        raise RuntimeError(
            f"Converted panel counts do not match the catalog: "
            f"expected {expected}, found {converted}"
        )

    print(
        f"Generated {converted['cube']} cube RGBA2222 intermediates in "
        f"{cube_rgba_dir}"
    )
    print(
        f"Generated {converted['sprite']} loose sprite RGBA2222 files in "
        f"{sprite_rgba_dir}"
    )


if __name__ == "__main__":
    db_path = 'build/data/build.db'
    panels_png_dir = 'build/panels/png'
    cube_rgba_dir = 'build/panels/rgba2'
    sprite_rgba_dir = 'tgt/panels'

    make_panels_rgba(
        db_path,
        panels_png_dir,
        cube_rgba_dir,
        sprite_rgba_dir,
    )
