-- SQLite
-- SELECT t2.render_obj_id, 'BUF_' || t2.panel_base_filename AS base_buffer_label, t1.tile_name, 
--     ROW_NUMBER() OVER (ORDER BY t2.render_obj_id)-1 AS sprite_img_idx
-- FROM tbl_02_tiles as t1
-- INNER JOIN qry_04_panels_lookup AS t2
-- ON t1.obj_id = t2.render_obj_id
-- WHERE t2.render_type = 'sprite' AND t2.face = 'south' AND t2.poly_id = 0
-- ORDER BY t2.render_obj_id, t2.poly_id;

-- SELECT t2.render_type, t2.render_obj_id, 'BUF_' || t2.panel_base_filename AS base_buffer_label, t1.tile_name, 
--     ROW_NUMBER() OVER (PARTITION BY t2.render_type ORDER BY t2.render_obj_id)-1 AS img_idx
-- FROM tbl_02_tiles as t1
-- INNER JOIN qry_04_panels_lookup AS t2
-- ON t1.obj_id = t2.render_obj_id
-- WHERE t2.face = 'south' AND t2.poly_id = 0
-- ORDER BY t2.render_type, t2.render_obj_id, t2.poly_id;

-- SELECT to_map_x, to_map_y, to_poly_id
-- FROM tbl_07_render_panels
-- WHERE floor_num = 0 AND map_x = 7 AND map_y = 14 and orientation = 0 and to_render_type = 'sprite'

-- SELECT t1.render_type, ROW_NUMBER() OVER (ORDER BY render_type)-1 AS render_type_idx
--         FROM (
--             SELECT DISTINCT render_type
--             FROM tbl_02_tiles
--             WHERE render_type NOT IN ('ui')
--         ) AS t1

SELECT t1.cell_id, t1.map_x, t1.map_y, t1.obj_id, t1.is_door, t1.is_wall, t1.is_trigger, t1.is_blocking, t1.render_type, t1.render_obj_id, t1.special, COALESCE(t2.img_idx,255) AS img_idx
FROM tbl_06_maps as t1
LEFT JOIN qry_02_img_idx as t2
ON t1.render_obj_id = t2.obj_id
WHERE floor_num = 0 AND room_id = 1 AND cell_id = 0
ORDER BY cell_id;