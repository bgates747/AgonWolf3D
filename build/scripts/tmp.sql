-- SQLite
-- SELECT floor_num, room_id, cell_id, map_x, map_y, obj_id, tile_name, is_active, is_door, is_wall, is_trigger, is_blocking, render_type, render_obj_id, scale, special, orientation, to_cell_id, to_map_x, to_map_y, to_obj_id, to_tile_name, to_is_active, to_is_door, to_is_wall, to_is_trigger, to_is_blocking, to_render_type, to_render_obj_id, to_scale, to_special, to_poly_id, to_cube_x, to_cube_y, to_r, to_g, to_b, to_mask_filename, to_plot_x, to_plot_y, to_dim_x, to_dim_y, to_face
-- FROM tbl_07_render_panels;

-- SELECT to_cell_id, to_map_x, to_map_y, to_obj_id, to_tile_name, to_render_obj_id, to_poly_id, to_cube_x, to_cube_y, to_face
-- FROM tbl_07_render_panels
-- WHERE (floor_num = 0 and room_id = 0 and map_x = 8 and map_y = 14 and orientation = 0)
-- or (to_cell_id = 221 and orientation = 0)
-- ORDER BY to_poly_id;

        SELECT t1.render_type, ROW_NUMBER() OVER (ORDER BY render_type)-1 AS render_type_idx
        FROM (
            SELECT DISTINCT render_type
            FROM tbl_02_tiles
            WHERE render_type NOT IN ('ui')
        ) AS t1