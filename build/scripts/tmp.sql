-- select count(*) as num_polys ; 45
-- from tbl_01_polys
-- ;

-- -- given poly is not blocking
-- with t1 as (
--     select poly_id, cube_y, poly_x0, poly_x1, face
--     from tbl_01_polys
-- ), t2 as (
--     select 
--         t1.poly_id as poly_id_1, 
--         t1.face as face_1,
--         t1.cube_y as cube_y_1, 
--         t1.poly_x0 as poly_x0_1, 
--         t1.poly_x1 as poly_x1_1,
--         t2.poly_id as poly_id_2, 
--         t2.face as face_2,
--         t2.cube_y as cube_y_2, 
--         t2.poly_x0 as poly_x0_2, 
--         t2.poly_x1 as poly_x1_2
--     from t1
--     inner join tbl_01_polys as t2 on 
--         (t1.cube_y < t2.cube_y and (t2.poly_x0 not between t1.poly_x0 and t1.poly_x1 or t2.poly_x1 not between t1.poly_x0 and t1.poly_x1))

--         or (t1.cube_y = t2.cube_y and t1.face = 'south' and t2.face <> 'south' and (t2.poly_x0 not between t1.poly_x0 and t1.poly_x1 or t2.poly_x1 not between t1.poly_x0 and t1.poly_x1))

--         or (t1.cube_y = t2.cube_y and t1.face = 'south' and t2.face = 'south')

--         or (t1.cube_y = t2.cube_y and t1.face <> 'south' and t2.face <> 'south')
-- ), t3 as (
--         select t2.*
--         from t1
--         inner join t2 on t1.poly_id = t2.poly_id_1
--         order by t1.poly_id desc, t2.poly_id_2 desc
-- )
-- select poly_id_2, count(*) as num_times_visible
-- from t3
-- group by poly_id_2
-- order by poly_id_2 desc

-- -- select *
-- -- from t3

-- -- select poly_id_1, count(*) as num_visible_polys, count(distinct cube_y_2) as num_visible_rows
-- -- from t3
-- -- group by poly_id_1
-- -- order by poly_id_1 desc
-- ;

-- -- given poly is blocking
-- with t1 as (
--     select poly_id, cube_y, poly_x0, poly_x1, face
--     from tbl_01_polys
-- ), t2 as (
--     select 
--         t1.poly_id as poly_id_1, 
--         t1.face as face_1,
--         t1.cube_y as cube_y_1, 
--         t1.poly_x0 as poly_x0_1, 
--         t1.poly_x1 as poly_x1_1,
--         t2.poly_id as poly_id_2, 
--         t2.face as face_2,
--         t2.cube_y as cube_y_2, 
--         t2.poly_x0 as poly_x0_2, 
--         t2.poly_x1 as poly_x1_2
--     from t1
--     inner join tbl_01_polys as t2 on 
--         (t1.cube_y < t2.cube_y and (t2.poly_x0 between t1.poly_x0 and t1.poly_x1 or t2.poly_x1 between t1.poly_x0 and t1.poly_x1))

--         or (t1.cube_y = t2.cube_y and t1.face = 'south' and t2.face <> 'south' and (t2.poly_x0 between t1.poly_x0 and t1.poly_x1 or t2.poly_x1 between t1.poly_x0 and t1.poly_x1))

--         or (t1.cube_y = t2.cube_y and t1.face = 'south' and t2.face = 'south')

--         or (t1.cube_y = t2.cube_y and t1.face <> 'south' and t2.face <> 'south')
-- ), t3 as (
--         select t2.*
--         from t1
--         inner join t2 on t1.poly_id = t2.poly_id_1
--         order by t1.poly_id desc, t2.poly_id_2 desc
-- )
-- select poly_id_2, count(*) as num_times_visible
-- from t3
-- group by poly_id_2
-- order by poly_id_2 desc
-- ;

-- select count(*) from tbl_01_polys; -- 45
-- select count(*) from tbl_01_polys where face = 'south' -- 25
-- ;

-- select t1.to_render_type, t1.to_is_blocking, t2.plot_x, t2.plot_y, t2.dim_x, t2.dim_y, t2.r, t2.g, t2.b
-- from qry_07_potential_panels as t1
-- inner join tbl_01_polys as t2 on t1.to_poly_id = t2.poly_id
-- where t1.floor_num = 0 and t1.map_x = 7 and t1.map_y = 14 and t1.orientation = 0
-- order by t1.to_poly_id

-- -- select to_render_type, to_is_blocking, to_plot_x, to_plot_y, to_dim_x, to_dim_y, to_r, to_g, to_b
-- select cell_id, to_cube_x, to_cube_y, to_poly_id, to_face, to_map_x, to_map_y, to_cell_id,
-- to_render_type, to_is_blocking102	137	57	45	45	127	191	153	020.png	sprite	24	50.0	bottom	center	24_020
-- from tbl_07_render_panels
-- -- from qry_07_potential_panels
-- where floor_num = 0 and room_id = 0 and map_x = 7 and map_y = 0 and orientation = 2
-- order by to_poly_id

-- select count(*) from tbl_04_panels_lookup;
-- select count(*) from tbl_04_panels_lookup;

-- select poly_id, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, plot_x, plot_y, dim_x, dim_y, scale, align_vert, align_horiz
-- from tbl_04_panels_lookup
-- where render_obj_id = 24;

-- select poly_id, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, plot_x, plot_y, dim_x, dim_y, scale, align_vert, align_horiz
-- from tbl_04_panels_lookup
-- where render_obj_id = 24;



-- select t1.cube_id, t1.poly_id, t1.face, t1.cube_x, t1.cube_y, 

--t1.poly_x0, t1.poly_y0, t1.poly_x1, t1.poly_y1, t1.poly_x2, t1.poly_y2, t1.poly_x3, t1.poly_y3, 

-- t1.plot_x + t2.plot_x - t3.plot_x as plot_x, 
-- t1.plot_y + t2.plot_y - t3.plot_y as plot_y, 

-- t3.plot_x, t3.plot_y

--t3.dim_x, t3.dim_y,

-- t2.dim_x, t2.dim_y


-- -- t1.r, t1.g, t1.b, t1.mask_filename, t1.render_type, t1.render_obj_id, t1.scale, t1.align_vert, t1.align_horiz, t1.panel_base_filename 
-- from (
--     select t1.*
--     from qry_04_panels_lookup as t1
--     left join tbl_04_panels_lookup as t2
--     on t1.render_obj_id = t2.render_obj_id and t1.poly_id = t2.poly_id
--     where t2.cube_id is null and t1.face = 'south'
-- ) as t1 inner join tbl_04_panels_lookup as t2
--     on t1.render_obj_id = t2.render_obj_id and t1.cube_y = t2.cube_y and t2.cube_x = 0
-- inner join tbl_01_polys as t3
--     on t2.poly_id = t3.poly_id
-- where t1.render_obj_id = 24
-- and t1.cube_y = 5
-- ;

-- -- select render_obj_id, face, poly_id, cube_x, cube_y, plot_x, plot_y, dim_x, dim_y
-- -- from tbl_04_panels_lookup
-- -- -- where poly_id = 41
-- -- where render_obj_id = 24
-- -- order by render_obj_id, poly_id

-- select cube_id, poly_id, cube_x, cube_y, render_obj_id, plot_x, plot_y, 'BUF_' || panel_base_filename as buffer_label
-- from tbl_04_panels_lookup
-- where render_type = 'sprite'
-- and render_obj_id = 24
-- order by render_obj_id, poly_id

-- select sprite_obj, south_id, render_obj_id, poly_id, cube_x, cube_y
-- from (
--     select row_number() over (order by render_obj_id) - 1 as sprite_obj, *
--     from tbl_02_tiles
--     where render_type = 'sprite' and is_active = 1
-- ) as t1 cross join (
--     select row_number() over (order by poly_id) - 1 as south_id, *
--     from tbl_01_polys
--     where face = 'south'
-- ) as t2
-- ;

-- select t1.poly_id, coalesce(t2.south_id,255) as south_id
-- from tbl_01_polys as t1
-- left join (
--     select poly_id, row_number() over (order by poly_id) - 1 as south_id, *
--     from tbl_01_polys
--     where face = 'south'
-- ) as t2 on t1.poly_id = t2.poly_id
-- order by t1.poly_id

-- delete from tbl_06_maps;

-- select obj_id, render_obj_id, count(*) as num_cells
-- from tbl_06_maps
-- group by obj_id, render_obj_id
-- order by obj_id, render_obj_id
-- ;

-- select t1.poly_id, t1.cube_x, t1.cube_y, t1.poly_x0, t1.poly_y0, t1.poly_x1, t1.poly_y1, t1.poly_x2, t1.poly_y2, t1.poly_x3, t1.poly_y3, t1.plot_x, t1.plot_y, t1.dim_x, t1.dim_y, t1.scale, t1.align_vert, t1.align_horiz, t2.plot_x, t2.plot_y, t2.dim_x, t2.dim_y, t2.scale, t2.align_vert, t2.align_horiz
-- from (
--     select poly_id, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, scale, align_vert, align_horiz
--     from tbl_04_panels_lookup
--     where render_obj_id = 51 and cube_x = 0
-- ) as t1 inner join (
--     select poly_id, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, scale, align_vert, align_horiz
--     from tbl_04_panels_lookup
--     where render_obj_id = 10 and cube_x = 0
-- ) as t2 on t1.poly_id = t2.poly_id
-- order by poly_id


select t1.poly_id, t1.cube_x, t1.cube_y, t1.poly_x0, t1.poly_y0, t1.poly_x1, t1.poly_y1, t1.poly_x2, t1.poly_y2, t1.poly_x3, t1.poly_y3, t1.plot_x, t1.plot_y, t1.dim_x, t1.dim_y, 
t2.plot_x as plot_x_unscaled, t2.plot_y as plot_y_unscaled, t2.dim_x dim_x_unscaled, t2.dim_y as dim_y_unscaled
from (
    select poly_id, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, scale, align_vert, align_horiz
    from tbl_04_panels_lookup
    where render_obj_id = 51 and cube_x = 0
) as t1 inner join (
    select poly_id, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, scale, align_vert, align_horiz
    from tbl_04_panels_lookup
    where render_obj_id = 10 and cube_x = 0
) as t2 on t1.poly_id = t2.poly_id
order by t1.poly_id desc