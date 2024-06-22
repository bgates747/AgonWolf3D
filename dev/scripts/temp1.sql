-- drop table if exists tbl_01_polys;
-- drop table if exists tbl_02_tiles;
-- drop table if exists tbl_06_maps;
-- drop table if exists tbl_07_potential_panels;
-- drop table if exists tbl_07_render_panels;
-- drop view if exists qry_01_polys;
-- drop view if exists qry_04_panels_lookup;
-- drop view if exists qry_07_map_orientations;
-- drop view if exists qry_07_map_polys;
-- drop view if exists qry_07_potential_panels;




-- DROP VIEW IF EXISTS qry_04_panels_lookup;
-- CREATE VIEW qry_04_panels_lookup AS
-- SELECT t1.cube_id, t1.poly_id, t1.face, t1.cube_x, t1.cube_y, t1.poly_x0, t1.poly_y0, t1.poly_x1, t1.poly_y1, t1.poly_x2, t1.poly_y2, t1.poly_x3, t1.poly_y3, t1.plot_x, t1.plot_y, t1.dim_x, t1.dim_y, t1.r, t1.g, t1.b, t1.mask_filename, t2.render_obj_id, 
-- t2.render_obj_id || '_' || printf('%03d', t1.panel_base_filename) as panel_base_filename
-- FROM qry_01_polys as t1
-- cross join (
--         select distinct coalesce(render_obj_id,obj_id) as render_obj_id
--         from tbl_02_tiles
--         where is_active = 1 and render_type = 'cube'
-- ) as t2
-- order by t2.render_obj_id, t1.poly_id;


-- select cube_id, poly_id, face, cube_x, cube_y, render_obj_id, panel_base_filename, mask_filename
-- from qry_04_panels_lookup
-- where face = 'south' and render_obj_id = 10
-- order by render_obj_id, poly_id;


-- SELECT t1.floor_num, t1.room_id, t1.cell_id, t1.orientation, t2.*, t2.render_obj_id || '_' || t2.panel_base_filename AS base_buffer_label
-- FROM tbl_07_render_panels as t1
-- INNER JOIN (
        -- SELECT t2.poly_id, t2.face, t2.cube_x, t2.cube_y, t2.plot_x, t2.plot_y, t2.dim_x, t2.dim_y, t2.mask_filename, t2.panel_base_filename, t1.render_obj_id, t3.tile_name as to_tile_name
        -- FROM qry_04_panels_lookup as t1
        -- INNER JOIN qry_01_polys as t2
        -- ON (t1.poly_id = t2.poly_id AND t1.face <> 'south')
        -- OR (t1.face = 'south' AND t2.face = 'south' AND t1.cube_y = t2.cube_y)
        -- INNER JOIN tbl_02_tiles as t3
        -- ON t1.render_obj_id = t3.obj_id
-- ) AS t2 ON t1.poly_id = t2.poly_id and t1.to_obj_id = t2.render_obj_id
-- WHERE t1.floor_num = {floor_num} AND t1.room_id = {room_id} AND t1.cell_id = {cell_id} AND t1.orientation = {orientation};

-- SELECT m.floor_num, m.room_id, m.cell_id, m.orientation,
-- FROM tbl_06_maps as m
-- LEFT JOIN  tbl_07_render_panels as P
-- ON m.floor_num = P.floor_num AND m.room_id = P.room_id AND m.cell_id = P.cell_id
-- -- INNER JOIN tbl_02_tiles as t
-- ;

-- -- SELECT 'BUF_' || pl.panel_base_filename AS panel_base_filename, rp.to_poly_id
-- SELECT rp.to_poly_id, rp.to_render_obj_id, pl.panel_base_filename
-- FROM tbl_07_render_panels AS rp
-- INNER JOIN qry_04_panels_lookup AS pl
-- ON rp.to_render_obj_id = pl.render_obj_id AND rp.to_poly_id = pl.poly_id
-- -- WHERE rp.floor_num = {floor_num} AND rp.room_id = {room_id} AND rp.cell_id = {cell_id} AND rp.orientation = {orientation}
-- ORDER BY rp.to_poly_id;

with cte as (
        select cube_y, CAST(max_x as REAL) - CAST(min_x AS REAL) as apparent_size
        from (
                select cube_y, min(poly_x) as min_x, max(poly_x) as max_x, min(poly_y) as min_y, max(poly_y) as max_y
                from tbl_00_polys_from_blender
                where face = 'south'
                group by cube_y
                order by cube_y
        ) as t1
), cte_sum as (
        select max(apparent_size) as max_apparent_size
        from cte
)
select cte.cube_y, cte.apparent_size / cte_sum.max_apparent_size as apparent_size
from cte, cte_sum