-- DROP TABLE IF EXISTS tbl_07_potential_panels;

-- CREATE TABLE tbl_07_potential_panels (
--     floor_num INTEGER,
--     room_id INTEGER,
--     cell_id INTEGER,
--     orientation INTEGER,
--     poly_id INTEGER,
--     cube_x INTEGER,
--     cube_y INTEGER,
--     mask_filename TEXT,
--     r INTEGER,
--     g INTEGER,
--     b INTEGER,
--     to_room_id INTEGER,
--     to_cell_id INTEGER,
--     to_map_x INTEGER,
--     to_map_y INTEGER,
--     to_obj_id INTEGER,
--     to_tile_name TEXT,
--     to_is_active INTEGER,
--     to_is_door INTEGER,
--     to_is_wall INTEGER,
--     to_is_trigger INTEGER,
--     to_is_blocking INTEGER,
--     to_render_type INTEGER,
--     to_render_as INTEGER,
--     to_scale INTEGER,
--     to_special TEXT
-- );

-- with t as (
--     select t1.*, t2.poly_id, t2.cube_x, t2.cube_y, t2.r, t2.g, t2.b, t2.mask_filename
--     from tbl_06_maps as t1
--     cross join tbl_01_polys_masks as t2
--     where t1.is_blocking = 1
-- ), f as (
--     select t1.*
--     from tbl_06_maps as t1
--     where t1.is_wall = 0 and t1.is_door = 0 and coalesce(special,' ') <> 'null cell'
-- ), p as (
--     select f.floor_num, f.room_id, f.cell_id, 0 as orientation, t.cube_x, t.cube_y, t.poly_id, t.mask_filename, t.r, t.g, t.b, t.room_id AS to_room_id, t.cell_id AS to_cell_id, t.map_x AS to_map_x, t.map_y AS to_map_y, t.obj_id AS to_obj_id, t.tile_name AS to_tile_name, t.is_active AS to_is_active, t.is_door AS to_is_door, t.is_wall AS to_is_wall, t.is_trigger AS to_is_trigger, t.is_blocking AS to_is_blocking, t.render_type AS to_render_type, t.render_as AS to_render_as, t.scale AS to_scale, t.special AS to_special
--     from f
--     inner join t
--         on f.floor_num = t.floor_num and f.room_id = t.room_id
--         and t.map_x = f.map_x + t.cube_x and t.map_y = f.map_y - t.cube_y
--     union all
--     select f.floor_num, f.room_id, f.cell_id, 1 as orientation, t.cube_x, t.cube_y, t.poly_id, t.mask_filename, t.r, t.g, t.b, t.room_id AS to_room_id, t.cell_id AS to_cell_id, t.map_x AS to_map_x, t.map_y AS to_map_y, t.obj_id AS to_obj_id, t.tile_name AS to_tile_name, t.is_active AS to_is_active, t.is_door AS to_is_door, t.is_wall AS to_is_wall, t.is_trigger AS to_is_trigger, t.is_blocking AS to_is_blocking, t.render_type AS to_render_type, t.render_as AS to_render_as, t.scale AS to_scale, t.special AS to_special
--     from f
--     inner join t
--         on f.floor_num = t.floor_num and f.room_id = t.room_id
--         and t.map_x = f.map_x + t.cube_y and t.map_y = f.map_y + t.cube_x
--     union all
--     select f.floor_num, f.room_id, f.cell_id, 2 as orientation, t.cube_x, t.cube_y, t.poly_id, t.mask_filename, t.r, t.g, t.b, t.room_id AS to_room_id, t.cell_id AS to_cell_id, t.map_x AS to_map_x, t.map_y AS to_map_y, t.obj_id AS to_obj_id, t.tile_name AS to_tile_name, t.is_active AS to_is_active, t.is_door AS to_is_door, t.is_wall AS to_is_wall, t.is_trigger AS to_is_trigger, t.is_blocking AS to_is_blocking, t.render_type AS to_render_type, t.render_as AS to_render_as, t.scale AS to_scale, t.special AS to_special
--     from f
--     inner join t
--         on f.floor_num = t.floor_num and f.room_id = t.room_id
--         and t.map_x = f.map_x - t.cube_x and t.map_y = f.map_y + t.cube_y
--     union all
--     select f.floor_num, f.room_id, f.cell_id, 3 as orientation, t.cube_x, t.cube_y, t.poly_id, t.mask_filename, t.r, t.g, t.b, t.room_id AS to_room_id, t.cell_id AS to_cell_id, t.map_x AS to_map_x, t.map_y AS to_map_y, t.obj_id AS to_obj_id, t.tile_name AS to_tile_name, t.is_active AS to_is_active, t.is_door AS to_is_door, t.is_wall AS to_is_wall, t.is_trigger AS to_is_trigger, t.is_blocking AS to_is_blocking, t.render_type AS to_render_type, t.render_as AS to_render_as, t.scale AS to_scale, t.special AS to_special
--     from f
--     inner join t
--         on f.floor_num = t.floor_num and f.room_id = t.room_id
--         and t.map_x = f.map_x - t.cube_y and t.map_y = f.map_y - t.cube_x
-- )

-- INSERT INTO tbl_07_potential_panels (floor_num, room_id, cell_id, orientation, poly_id, cube_x, cube_y, mask_filename, r, g, b, to_room_id, to_cell_id, to_map_x, to_map_y, to_obj_id, to_tile_name, to_is_active, to_is_door, to_is_wall, to_is_trigger, to_is_blocking, to_render_type, to_render_as, to_scale, to_special)
-- select floor_num, room_id, cell_id, orientation, poly_id, cube_x, cube_y, mask_filename, r, g, b, to_room_id, to_cell_id, to_map_x, to_map_y, to_obj_id, to_tile_name, to_is_active, to_is_door, to_is_wall, to_is_trigger, to_is_blocking, to_render_type, to_render_as, to_scale, to_special
-- from p
-- order by floor_num, room_id, cell_id, orientation, poly_id
-- ;

-- SELECT floor_num, room_id, cell_id, orientation, poly_id, cube_x, cube_y, mask_filename, r, g, b, to_room_id, to_cell_id, to_map_x, to_map_y, to_obj_id, to_tile_name, to_is_active, to_is_door, to_is_wall, to_is_trigger, to_is_blocking, to_render_type, to_render_as, to_scale, to_special
-- FROM tbl_07_potential_panels
-- where to_is_blocking = 0;

-- SELECT
--   (SELECT COUNT(*) FROM tbl_07_potential_panels) AS potential,
--   (SELECT COUNT(*) FROM tbl_07_render_panels) AS render;


-- select t1.*, t2.plot_x, t2.plot_y, t2.dim_x, t2.dim_y, 
--     t1.to_obj_id || '_' || REPLACE(t1.mask_filename, '.png', '.rgba') AS panel_filename
-- from tbl_07_render_panels as t1
-- inner join tbl_01_polys_masks as t2
--     on t1.poly_id = t2.poly_id
-- order by t1.floor_num, t1.room_id, t1.cell_id, t1.orientation, t1.poly_id
-- ;

-- select distinct render_type, render_as, scale, special
-- select floor_num, room_id, cell_id, map_x, map_y, obj_id, tile_name, is_active, is_door, is_wall, is_trigger, is_blocking, render_type, render_as, scale, special
-- from tbl_06_maps
-- where is_active = 1 and is_door = 0 and is_wall = 0 and special <> 'null cell' and render_type <> 'cube';

 --and render_type = 'floor'


-- select t2.poly_id, t2.plot_x, t2.plot_y, 
--     t2.dim_x, t1.dim_x as real_dim_x, 
--     t2.dim_y, t1.dim_y as real_dim_y
-- from (
--     SELECT DISTINCT CAST(SUBSTR(filename, -3) AS INTEGER) AS poly_id, dim_x, dim_y
--     FROM tbl_05_panel_dims
-- ) as t1
-- inner join tbl_01_polys_masks as t2
--     on t1.poly_id = t2.poly_id
-- order by t2.poly_id desc;
-- where t1.dim_x <> t2.dim_x or t1.dim_y <> t2.dim_y

-- select panel_base_filename, count(*) as num_dims
-- from (
--     select distinct panel_base_filename, dim_x, dim_y
--     from qry_01_polys_masks
-- ) as t1
-- group by panel_base_filename
-- order by num_dims desc;

-- select t2.poly_id, t2.plot_x, t2.plot_y, 
--     t2.dim_x, t1.dim_x as real_dim_x, 
--     t2.dim_y, t1.dim_y as real_dim_y
-- from (
--     SELECT DISTINCT SUBSTR(filename, -3) || '.png' AS panel_base_filename, dim_x, dim_y
--     FROM tbl_05_panel_dims
-- ) as t1 inner join qry_01_polys_masks as t2
--     on t1.panel_base_filename = t2.panel_base_filename
-- -- where t1.dim_x <> t2.dim_x or t1.dim_y <> t2.dim_y
-- order by t2.poly_id desc;

-- select *
-- from tbl_06_maps
-- where room_id = 0
-- order by cell_id
-- ;

PRAGMA table_info(tbl_02_tiles);