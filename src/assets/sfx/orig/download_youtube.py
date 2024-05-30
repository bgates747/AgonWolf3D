import os
from pydub import AudioSegment
from pydub import effects
from pytube import YouTube
from playsound import playsound

def play_sound(filename, is_blocking):
    playsound(filename, block=is_blocking)

def get_youtube_audio(song_url, saved_songs_dir, normalize_levels=False):
    yt = YouTube(song_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    song_filename = audio_stream.default_filename
    input_file = os.path.join(saved_songs_dir, song_filename)
    base_filename = os.path.splitext(input_file)[0]
    output_file = f"{base_filename}.ogg"

    # Download the audio stream
    audio_stream.download(saved_songs_dir)
    # Convert to ogg
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format="ogg")
    os.remove(input_file)  # Cleanup original file

    if normalize_levels:
        # Normalize audio levels
        audio = AudioSegment.from_file(output_file)
        audio = effects.normalize(audio)
        audio.export(output_file, format="ogg")

    return audio, output_file

def convert_audio_to_pcm(audio, output_path):
    # Resample the audio to 16000 Hz
    resampled_audio = audio.set_frame_rate(16000)
    # Mix stereo to mono
    resampled_audio = resampled_audio.set_channels(1)
    # Convert audio to 8-bit PCM
    pcm_audio = resampled_audio.set_sample_width(1)  # Set sample width to 1 byte (8 bits)
    # Export as raw PCM
    pcm_audio.export(output_path, format="pcm_s8")

import librosa
import numpy as np
from pydub import AudioSegment

def convert_audio_to_pcm_librosa(audio, output_path):
    # Convert AudioSegment to NumPy array
    samples = np.array(audio.get_array_of_samples())
    sample_rate = audio.frame_rate
    
    # Resample using librosa
    resampled_samples = librosa.resample(samples.astype(float), orig_sr=sample_rate, target_sr=16000)

    # Create a new AudioSegment from the resampled data
    resampled_audio = AudioSegment(
        data=resampled_samples.astype(np.int16).tobytes(),
        sample_width=2,
        frame_rate=16000,
        channels=1
    )

    # Convert to 8-bit PCM
    pcm_audio = resampled_audio.set_sample_width(1)

    # Export as raw PCM
    pcm_audio.export(output_path, codec="pcm_s8")

    return output_path

import subprocess

def convert_ogg_to_pcm(input_file, output_file):
    # Construct the ffmpeg command
    command = [
        'ffmpeg',
        '-i', input_file,             # Input file
        '-ac', '1',                   # Set audio channels to 1 (mono)
        '-ar', '16000',               # Resample to 16000 Hz
        '-f', 's8',                   # Format set to signed 8-bit PCM
        '-acodec', 'pcm_s8',          # Audio codec set to PCM signed 8-bit
        output_file                   # Output file
    ]

    # Execute the command
    subprocess.run(command, check=False)

if __name__ == '__main__':
    # Paths and URL setup
    saved_songs_dir = 'src/assets/sfx/orig'
    # song_url = 'https://www.youtube.com/watch?v=7A9MfVRFMC8' # pickup treasure
    # song_url = 'https://www.youtube.com/watch?v=L-dB_kT34m8' # all the things
    # song_url = 'https://www.youtube.com/watch?v=G_g72yHhIiI' # the full Wilhelm scream!!!111
    # song_url = 'https://www.youtube.com/watch?v=M6z4fJTw1Xo' # gun empty click
    song_url = 'https://youtu.be/y-RCKubsfpg' # shotgun reload

    audio, output_file_ogg = get_youtube_audio(song_url, saved_songs_dir)
    # output_file_raw = output_file_ogg.replace('.ogg', '.raw')
    # convert_audio_to_pcm(audio, output_file)
    # convert_audio_to_pcm_librosa(audio, output_file)
    # convert_ogg_to_pcm(output_file_ogg, output_file_raw)

