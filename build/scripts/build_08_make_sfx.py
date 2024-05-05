import os
import sqlite3
import shutil

def make_tbl_08_sfx(conn, cursor):
    cursor.execute("""
        drop table if exists tbl_08_sfx;""")
    conn.commit()
    cursor.execute("""
        create table if not exists tbl_08_sfx (
            sfx_id integer,
            size integer,
            duration integer,
            filename text,
            primary key (sfx_id)
        );""")
    conn.commit()

def make_sfx(db_path, src_dir, tgt_dir):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    make_tbl_08_sfx(conn, cursor)

    if os.path.exists(tgt_dir):
        shutil.rmtree(tgt_dir)
    os.makedirs(tgt_dir)

    sfxs = []
    for filename in sorted(os.listdir(src_dir)):
        if filename.endswith('.raw'):
            sfxs.append((len(sfxs) + 0, filename))

    for sfx in sfxs:
        sfx_id, filename = sfx
        src_path = os.path.join(src_dir, filename)
        tgt_path = os.path.join(tgt_dir, filename)
        shutil.copy(src_path, tgt_path)
        size = os.path.getsize(src_path)
        duration = size // 16
        cursor.execute("""
            insert into tbl_08_sfx (sfx_id, size, duration, filename)
            values (?, ?, ?, ?);""", (sfx_id, size, duration, filename))
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    db_path = 'build/data/build.db'
    src_dir = 'src/assets/sfx'
    tgt_dir = 'tgt/sfx'

    make_sfx(db_path, src_dir, tgt_dir)

