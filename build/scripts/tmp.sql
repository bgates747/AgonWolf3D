-- SQLite
-- DROP TABLE IF EXISTS tbl_91a_font_itc_honda;
-- DROP TABLE IF EXISTS tbl_91a_font;

-- delete from tbl_91a_font where font_name is null;

SELECT font_name, char_num, plot_x, y_offset, dim_x, dim_y, img_filename
FROM tbl_91a_font;