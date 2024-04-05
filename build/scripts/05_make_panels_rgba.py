from agonImages import img_to_rgba2, convert_to_agon_palette
import os
import shutil
import PIL as pillow
import sqlite3

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    panels_src_dir = 'build/panels/png'
    panels_dst_dir = 'tgt/panels'

    image_width = 320
    image_height = 160

    # Delete the target directory if it exists and recreate it
    if os.path.exists(panels_dst_dir):
        shutil.rmtree(panels_dst_dir)
    os.makedirs(panels_dst_dir)

    # generate a list of files in the source directory
    files = os.listdir(panels_src_dir)
    files.sort()
    for file in files:
        # open file as a PIL image
        img = pillow.Image.open(os.path.join(panels_src_dir, file))
        # img = convert_to_agon_palette(img, 64, "HSV")
        # generate target filepath
        filename = os.path.splitext(file)[0].replace(".png", "")
        tgt_filepath = os.path.join(panels_dst_dir, filename) + ".rgba"
        # convert the image to RGBA
        img_rgba = img_to_rgba2(img,tgt_filepath)

        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create the tbl_05_panel_dims table
        cursor.execute('DROP TABLE IF EXISTS tbl_05_panel_dims')
        conn.commit()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tbl_05_panel_dims (
                filename TEXT NOT NULL,
                dim_x INTEGER NOT NULL,
                dim_y INTEGER NOT NULL,
            primary key (filename)
            )
        ''')
        conn.commit()

        # Iterate over the files and insert their dimensions into the table
        for file in files:
            # Open file as a PIL image
            img = pillow.Image.open(os.path.join(panels_src_dir, file))
            # Get the dimensions of the image
            width, height = img.size
            # Get the filename without the extension
            filename = os.path.splitext(file)[0].replace(".png", "")
            # Insert the dimensions into the table
            cursor.execute('''
                INSERT INTO tbl_05_panel_dims (filename, dim_x, dim_y)
                VALUES (?, ?, ?)
            ''', (filename, width, height))

        # Commit the changes and close the connection
        conn.commit()

        # # Create a cursor and execute the query
        # cursor = conn.cursor()
        # cursor.execute('''
        #     select t2.poly_id, t2.plot_x, t2.plot_y, 
        #         t2.dim_x, t1.dim_x as real_dim_x, 
        #         t2.dim_y, t1.dim_y as real_dim_y
        #     from (
        #         SELECT DISTINCT SUBSTR(filename, -3) || '.png' AS panel_base_filename, dim_x, dim_y
        #         FROM tbl_05_panel_dims
        #     ) as t1 inner join qry_01_polys_masks as t2
        #         on t1.panel_base_filename = t2.panel_base_filename
        #     where t1.dim_x <> t2.dim_x or t1.dim_y <> t2.dim_y
        # ''')

        # # Iterate over the results and update tbl_01_polys_masks with the real dimensions
        # for row in cursor.fetchall():
        #     poly_id = row[0]
        #     real_dim_x = row[4]
        #     real_dim_y = row[6]
            
        #     cursor.execute('''
        #         UPDATE tbl_01_polys_masks
        #         SET dim_x = ?, dim_y = ?
        #         WHERE poly_id = ?
        #     ''', (real_dim_x, real_dim_y, poly_id))

        # # Commit the changes and close the cursor
        # conn.commit()
        # cursor.close()

        # # Open another cursor to update tbl_01_polys_masks
        # cursor_update = conn.cursor()

        # cursor_update.execute('''
        #     UPDATE tbl_01_polys_masks
        #     SET plot_y = (? - dim_y) / 2
        # ''', (image_height,))

        # conn.commit()

        # # Set any plot_x values that are less than 0 to 0
        # cursor_update.execute('''
        #     UPDATE tbl_01_polys_masks
        #     SET plot_x = 0
        #     WHERE plot_x < 0
        # ''')

        # # Commit the changes and close the cursor
        # conn.commit()
        # cursor_update.close()

        conn.close()