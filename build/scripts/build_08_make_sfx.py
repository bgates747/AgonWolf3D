import os
import sqlite3
import shutil
import subprocess

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
        if filename.endswith('.wav'):
            filename = filename.replace('.wav', '.raw')
            sfxs.append((len(sfxs) + 0, filename))

    for sfx in sfxs:
        sfx_id, filename = sfx
        src_path = os.path.join(src_dir, filename.replace('.raw', '.wav'))
        tgt_path = os.path.join(tgt_dir, filename)

        # Construct the ffmpeg command
        command = [
            'ffmpeg',
            '-i', src_path,             # Input file
            '-ac', '1',                   # Set audio channels to 1 (mono)
            '-ar', '16384',               # Resample to 16000 Hz
            '-f', 's8',                   # Format set to signed 8-bit PCM
            '-acodec', 'pcm_s8',          # Audio codec set to PCM signed 8-bit
            tgt_path                   # Output file
        ]

        # Execute the command
        subprocess.run(command, check=False)

        size = os.path.getsize(tgt_path)
        duration = size // 16.384
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

