-- SQLite
-- SELECT cube_id, poly_id, face, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, r, g, b, mask_filename
-- FROM tbl_01_polys
-- ORDER BY poly_id;

-- select floor_num, room_id, cell_id, map_x, map_y, obj_id, tile_name, is_active, is_door, is_wall, is_trigger, is_blocking, render_type, render_obj_id, scale, align_vert, align_horiz, special, orientation, to_cell_id, to_map_x, to_map_y, to_obj_id, to_tile_name, to_is_active, to_is_door, to_is_wall, to_is_trigger, to_is_blocking, to_render_type, to_render_obj_id, to_scale, to_special, to_poly_id, to_cube_x, to_cube_y, to_r, to_g, to_b, to_mask_filename, to_plot_x, to_plot_y, to_dim_x, to_dim_y, to_face

-- select floor_num, room_id, cell_id, orientation, count(*) as num_cells
-- from qry_07_potential_panels
-- group by floor_num, room_id, cell_id, orientation
-- order by floor_num, room_id, cell_id, orientation;

-- select floor_num, room_id, cell_id, orientation, count(*) as num_cells
-- from tbl_07_render_panels
-- group by floor_num, room_id, cell_id, orientation
-- order by floor_num, room_id, cell_id, orientation;

-- select 1 * coalesce(null,256);

-- select power(2,0);

select p.floor_num, p.room_id, p.cell_id, p.orientation, 
    sum(case when p.to_poly_id between 0 and 7 then power(2,r.to_poly_id) else 0 end) as mask_0,
    sum(case when p.to_poly_id between 8 and 15 then power(2,r.to_poly_id-8) else 0 end) as mask_1,
    sum(case when p.to_poly_id between 16 and 23 then power(2,r.to_poly_id-16) else 0 end) as mask_2,
    sum(case when p.to_poly_id between 24 and 31 then power(2,r.to_poly_id-24) else 0 end) as mask_3,
    sum(case when p.to_poly_id between 32 and 39 then power(2,r.to_poly_id-32) else 0 end) as mask_4,
    sum(case when p.to_poly_id between 40 and 47 then power(2,r.to_poly_id-40) else 0 end) as mask_5
from qry_07_potential_panels as p
left join tbl_07_render_panels as r 
on p.floor_num = r.floor_num and p.room_id = r.room_id and p.cell_id = r.cell_id and p.orientation = r.orientation and p.to_poly_id = r.to_poly_id
group by p.floor_num, p.room_id, p.cell_id, p.orientation
order by p.floor_num, p.room_id, p.cell_id, p.orientation;