from agonImages import img_to_rgba2, convert_to_agon_palette
import os
import shutil
import PIL as pillow
import sqlite3

def make_panels_rgba(db_path, panels_png_dir, panels_rgba_dir, image_height):
    # Ensure the target directory exists
    if os.path.exists(panels_rgba_dir):
        shutil.rmtree(panels_rgba_dir)
    os.makedirs(panels_rgba_dir)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Prepare the database: drop and recreate tbl_05_panel_dims
    cursor.execute('DROP TABLE IF EXISTS tbl_05_panel_dims')
    cursor.execute('''
        CREATE TABLE tbl_05_panel_dims (
            filename TEXT NOT NULL,
            dim_x INTEGER NOT NULL,
            dim_y INTEGER NOT NULL,
            PRIMARY KEY (filename)
        )
    ''')
    conn.commit()

    # Process each PNG file
    files = sorted(os.listdir(panels_png_dir))
    for file in files:
        if file.endswith(".png"):
            img = pillow.Image.open(os.path.join(panels_png_dir, file))
            # img = convert_to_agon_palette(img, 64, "HSV")
            filename = os.path.splitext(file)[0]
            tgt_filepath = os.path.join(panels_rgba_dir, filename) + ".rgba"
            img_rgba = img_to_rgba2(img, tgt_filepath)

            # Insert image dimensions into tbl_05_panel_dims
            width, height = img.size
            cursor.execute('''
                INSERT INTO tbl_05_panel_dims (filename, dim_x, dim_y)
                VALUES (?, ?, ?)
            ''', (filename, width, height))

    conn.commit()  # Commit after processing all files

    # Code to update tbl_01_polys_masks with the real dimensions and adjust plot positions
    cursor.execute('''
        SELECT t2.poly_id, t2.plot_x, t2.plot_y, t2.dim_x, t1.dim_x AS real_dim_x, 
               t2.dim_y, t1.dim_y AS real_dim_y
        FROM (
            SELECT DISTINCT SUBSTR(filename, -3) || '.png' AS panel_base_filename, dim_x, dim_y
            FROM tbl_05_panel_dims
        ) AS t1
        INNER JOIN qry_01_polys_masks AS t2 ON t1.panel_base_filename = t2.panel_base_filename
        WHERE t1.dim_x <> t2.dim_x OR t1.dim_y <> t2.dim_y
    ''')

    for row in cursor.fetchall():
        cursor.execute('''
            UPDATE tbl_01_polys_masks
            SET dim_x = ?, dim_y = ?
            WHERE poly_id = ?
        ''', (row[4], row[6], row[0]))

    cursor.execute('''
        UPDATE tbl_01_polys_masks
        SET plot_y = (? - dim_y) / 2, plot_x = CASE WHEN plot_x < 0 THEN 0 ELSE plot_x END
    ''', (image_height,))

    conn.commit()  # Commit the changes
    cursor.close()  # Close the cursor
    conn.close()  # Close the database connection

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    panels_png_dir = 'build/panels/png'
    panels_rgba_dir = 'tgt/panels'
    image_height = 160

    make_panels_rgba(db_path, panels_png_dir, panels_rgba_dir, image_height)


# from agonImages import img_to_rgba2, convert_to_agon_palette
# import os
# import shutil
# import PIL as pillow
# import sqlite3

# def make_panels_rgba(db_path, panels_png_dir, panels_rgba_dir):

#     # Delete the target directory if it exists and recreate it
#     if os.path.exists(panels_rgba_dir):
#         shutil.rmtree(panels_rgba_dir)
#     os.makedirs(panels_rgba_dir)

#     # generate a list of files in the source directory
#     files = os.listdir(panels_png_dir)
#     files.sort()
#     for file in files:
#         # open file as a PIL image
#         img = pillow.Image.open(os.path.join(panels_png_dir, file))
#         # img = convert_to_agon_palette(img, 64, "HSV")
#         # generate target filepath
#         filename = os.path.splitext(file)[0].replace(".png", "")
#         tgt_filepath = os.path.join(panels_rgba_dir, filename) + ".rgba"
#         # convert the image to RGBA
#         img_rgba = img_to_rgba2(img,tgt_filepath)

#         # Connect to the SQLite database
#         conn = sqlite3.connect(db_path)
#         cursor = conn.cursor()

#         # Create the tbl_05_panel_dims table
#         cursor.execute('DROP TABLE IF EXISTS tbl_05_panel_dims')
#         conn.commit()

#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS tbl_05_panel_dims (
#                 filename TEXT NOT NULL,
#                 dim_x INTEGER NOT NULL,
#                 dim_y INTEGER NOT NULL,
#             primary key (filename)
#             )
#         ''')
#         conn.commit()

#         # Iterate over the files and insert their dimensions into the table
#         for file in files:
#             # Open file as a PIL image
#             img = pillow.Image.open(os.path.join(panels_png_dir, file))
#             # Get the dimensions of the image
#             width, height = img.size
#             # Get the filename without the extension
#             filename = os.path.splitext(file)[0].replace(".png", "")
#             # Insert the dimensions into the table
#             cursor.execute('''
#                 INSERT INTO tbl_05_panel_dims (filename, dim_x, dim_y)
#                 VALUES (?, ?, ?)
#             ''', (filename, width, height))

#         # Commit the changes and close the connection
#         conn.commit()

#         # Close the cursor
#         cursor.close()

# if __name__ == "__main__":
#     db_path = 'build/data/build.db'
#     panels_png_dir = 'build/panels/png'
#     panels_rgba_dir = 'tgt/panels'
#     image_width = 320
#     image_height = 160

#     make_panels_rgba(db_path, panels_png_dir, panels_rgba_dir)

#         # Create a cursor and execute the query
#         cursor = conn.cursor()
#         cursor.execute('''
#             select t2.poly_id, t2.plot_x, t2.plot_y, 
#                 t2.dim_x, t1.dim_x as real_dim_x, 
#                 t2.dim_y, t1.dim_y as real_dim_y
#             from (
#                 SELECT DISTINCT SUBSTR(filename, -3) || '.png' AS panel_base_filename, dim_x, dim_y
#                 FROM tbl_05_panel_dims
#             ) as t1 inner join qry_01_polys_masks as t2
#                 on t1.panel_base_filename = t2.panel_base_filename
#             where t1.dim_x <> t2.dim_x or t1.dim_y <> t2.dim_y
#         ''')

#         # Iterate over the results and update tbl_01_polys_masks with the real dimensions
#         for row in cursor.fetchall():
#             poly_id = row[0]
#             real_dim_x = row[4]
#             real_dim_y = row[6]
            
#             cursor.execute('''
#                 UPDATE tbl_01_polys_masks
#                 SET dim_x = ?, dim_y = ?
#                 WHERE poly_id = ?
#             ''', (real_dim_x, real_dim_y, poly_id))

#         # Commit the changes and close the cursor
#         conn.commit()
#         cursor.close()

#         # Open another cursor to update tbl_01_polys_masks
#         cursor_update = conn.cursor()

#         cursor_update.execute('''
#             UPDATE tbl_01_polys_masks
#             SET plot_y = (? - dim_y) / 2
#         ''', (image_height,))

#         conn.commit()

#         # Set any plot_x values that are less than 0 to 0
#         cursor_update.execute('''
#             UPDATE tbl_01_polys_masks
#             SET plot_x = 0
#             WHERE plot_x < 0
#         ''')

#         # Commit the changes and close the cursor
#         conn.commit()
#         cursor_update.close()