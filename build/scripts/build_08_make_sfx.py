import os
import sqlite3
import shutil
import subprocess
import wave

def make_tbl_08_sfx(conn, cursor):
    cursor.execute("""
        drop table if exists tbl_08_sfx;""")
    conn.commit()
    cursor.execute("""
        create table if not exists tbl_08_sfx (
            sfx_id integer,
            size integer,
            duration integer,
            sample_rate integer,
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
            filename = filename
            sfxs.append((len(sfxs) + 0, filename))

    for sfx in sfxs:
        sfx_id, filename = sfx
        src_path = os.path.join(src_dir, filename)
        tgt_path = os.path.join(tgt_dir, filename)

        # Construct the ffmpeg command
        command = [
            'ffmpeg',
            '-hide_banner',
            '-loglevel', 'error',
            '-y',
            '-i', src_path,             # Input file
            '-ac', '1',                   # Set audio channels to 1 (mono)
            '-acodec', 'pcm_u8',          # Unsigned 8-bit PCM required by AGNB 0.2
            tgt_path                   # Output file
        ]

        # Execute the command
        subprocess.run(command, check=True)

        with wave.open(tgt_path, 'rb') as wav:
            sample_rate = wav.getframerate()
            size = wav.getnframes()
            duration = int(size * 1000 / sample_rate)
        cursor.execute("""
            insert into tbl_08_sfx
                (sfx_id, size, duration, sample_rate, filename)
            values (?, ?, ?, ?, ?);""",
            (sfx_id, size, duration, sample_rate, filename))
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    db_path = 'build/data/build.db'
    src_dir = 'src/assets/sfx'
    tgt_dir = 'build/sfx/wav'

    make_sfx(db_path, src_dir, tgt_dir)
