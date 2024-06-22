-- SELECT * FROM tbl_02_tiles
-- WHERE special = 'outer';

-- select *
-- -- delete
-- from tbl_06_maps;

-- delete from tbl_07_render_panels;
-- delete from tbl_07_potential_panels;

select *
from tbl_06_maps
where floor_num = 0;

select t1.floor_num, t1.room_id, t1.cell_id, t2.map_x, t2.map_y, count(*) as num_panels
from tbl_07_render_panels as t1
left join tbl_06_maps as t2
on t1.floor_num = t2.floor_num and t1.room_id = t2.room_id and t1.cell_id = t2.cell_id
group by t1.floor_num, t1.room_id, t1.cell_id, t2.map_x, t2.map_y
ORDER BY t1.floor_num, t1.room_id, t1.cell_id
;

-- select *
-- from tbl_07_potential_panels;

-- select *
-- from tbl_07_render_panels;

        -- with t as (
        --     select t1.*, t2.poly_id, t2.cube_x, t2.cube_y, t2.r, t2.g, t2.b, t2.mask_filename
        --     from tbl_06_maps as t1
        --     cross join tbl_01_polys as t2
        --     where t1.floor_num = 0
        -- ), f as (
        --     select t1.*
        --     from tbl_06_maps as t1
        --     where t1.floor_num = 0 and t1.is_wall = 0 and t1.is_door = 0 and coalesce(special,' ') <> 'null cell'
        -- ), p as (
        
        --     select f.floor_num, f.room_id, f.cell_id, 0 as orientation, t.cube_x, t.cube_y, t.poly_id, t.mask_filename, t.r, t.g, t.b, t.room_id AS to_room_id, t.cell_id AS to_cell_id, t.map_x AS to_map_x, t.map_y AS to_map_y, t.obj_id AS to_obj_id, t.tile_name AS to_tile_name, t.is_active AS to_is_active, t.is_door AS to_is_door, t.is_wall AS to_is_wall, t.is_trigger AS to_is_trigger, t.is_blocking AS to_is_blocking, t.render_type AS to_render_type, t.render_obj_id AS to_render_obj_id, t.scale AS to_scale, t.special AS to_special
        --     from f
        --     inner join t
        --         on f.floor_num = t.floor_num and f.room_id = t.room_id
        --             and t.map_x = (f.map_x + t.cube_x) % 16
        --             and t.map_y = (f.map_y - t.cube_y) % 16

        --     union all

        --     select f.floor_num, f.room_id, f.cell_id, 1 as orientation, t.cube_x, t.cube_y, t.poly_id, t.mask_filename, t.r, t.g, t.b, t.room_id AS to_room_id, t.cell_id AS to_cell_id, t.map_x AS to_map_x, t.map_y AS to_map_y, t.obj_id AS to_obj_id, t.tile_name AS to_tile_name, t.is_active AS to_is_active, t.is_door AS to_is_door, t.is_wall AS to_is_wall, t.is_trigger AS to_is_trigger, t.is_blocking AS to_is_blocking, t.render_type AS to_render_type, t.render_obj_id AS to_render_obj_id, t.scale AS to_scale, t.special AS to_special
        --     from f
        --     inner join t
        --         on f.floor_num = t.floor_num and f.room_id = t.room_id
        --             and t.map_x = (f.map_x + t.cube_y) % 16
        --             and t.map_y = (f.map_y + t.cube_x) % 16

        --     union all

        --     select f.floor_num, f.room_id, f.cell_id, 2 as orientation, t.cube_x, t.cube_y, t.poly_id, t.mask_filename, t.r, t.g, t.b, t.room_id AS to_room_id, t.cell_id AS to_cell_id, t.map_x AS to_map_x, t.map_y AS to_map_y, t.obj_id AS to_obj_id, t.tile_name AS to_tile_name, t.is_active AS to_is_active, t.is_door AS to_is_door, t.is_wall AS to_is_wall, t.is_trigger AS to_is_trigger, t.is_blocking AS to_is_blocking, t.render_type AS to_render_type, t.render_obj_id AS to_render_obj_id, t.scale AS to_scale, t.special AS to_special
        --     from f
        --     inner join t
        --         on f.floor_num = t.floor_num and f.room_id = t.room_id
        --             and t.map_x = (f.map_x - t.cube_x) % 16
        --             and t.map_y = (f.map_y + t.cube_y) % 16

        --     union all

        --     select f.floor_num, f.room_id, f.cell_id, 3 as orientation, t.cube_x, t.cube_y, t.poly_id, t.mask_filename, t.r, t.g, t.b, t.room_id AS to_room_id, t.cell_id AS to_cell_id, t.map_x AS to_map_x, t.map_y AS to_map_y, t.obj_id AS to_obj_id, t.tile_name AS to_tile_name, t.is_active AS to_is_active, t.is_door AS to_is_door, t.is_wall AS to_is_wall, t.is_trigger AS to_is_trigger, t.is_blocking AS to_is_blocking, t.render_type AS to_render_type, t.render_obj_id AS to_render_obj_id, t.scale AS to_scale, t.special AS to_special
        --     from f
        --     inner join t
        --         on f.floor_num = t.floor_num and f.room_id = t.room_id
        --             and t.map_x = (f.map_x - t.cube_y) % 16
        --             and t.map_y = (f.map_y - t.cube_x) % 16
        -- )
        -- select floor_num, room_id, cell_id, orientation, poly_id, cube_x, cube_y, mask_filename, r, g, b, to_room_id, to_cell_id, to_map_x, to_map_y, to_obj_id, to_tile_name, to_is_active, to_is_door, to_is_wall, to_is_trigger, to_is_blocking, to_render_type, to_render_obj_id, to_scale, to_special
        -- from p
        -- order by floor_num, room_id, cell_id, orientation, poly_id