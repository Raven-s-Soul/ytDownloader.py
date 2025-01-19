from pytubefix import Playlist, YouTube
from pytubefix.cli import on_progress
import re  # Import the 're' module for regular expressions
import os
import subprocess

#Combines video and audio streams using FFmpeg
def combine_streams(video_path, audio_path, output_path):
    try:
        subprocess.run(
            [
                'ffmpeg',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-strict', 'experimental',
                output_path
            ],
            check=True
        )
        print(f"Combined video saved: {output_path}")
    except subprocess.CalledProcessError:
        print("FFmpeg failed to combine audio and video. Please ensure it is installed.")
    finally:
        os.remove(video_path)
        os.remove(audio_path)

def download_video(video):
    try:
        # Create a YouTube object
        yt = YouTube(video, 'WEB', on_progress_callback=on_progress)  # use_po_token=True
        print(f"Downloading video: {yt.title}")

        # Get the stream with the highest resolution (may be adaptive)
        video_stream = yt.streams.get_highest_resolution(False)
        print(f"Selected video stream: {video_stream.resolution} ({video_stream.fps}fps)")

        # Check if the stream is adaptive
        if not video_stream.is_progressive:
            # Get the audio stream with the best quality
            audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            print(f"Selected audio stream: {audio_stream.abr}")

            if not audio_stream:
                raise Exception('No suitable audio stream found.')
            
            video_name = f"video_{yt.title}.mp4"
            audio_name = f"audio_{yt.title}.mp4"
            
            # Download the video and audio streams
            video_path = video_stream.download(filename=video_name)
            print(f"Video stream downloaded: {video_path}")
            audio_path = audio_stream.download(filename=audio_name)
            print(f"Audio stream downloaded: {audio_path}")
            
            output_path = f"{re.sub(r'[\\/*?:"<>|]', '', yt.title)}.mp4"
            combine_streams(video_path, audio_path, output_path)
        else:
            video_stream.download()
            print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")


def CoreLogic():
    isPlaylist = 0
    
    while isPlaylist not in {'y', 'n'}:
        isPlaylist = input("Type Y/y or N/n if it's a playlist: ").strip().lower()  
        
    url = input("Please enter the YouTube URL: ")
    
    if isPlaylist == 'y':
        pl = Playlist(url)
        for index, video in enumerate(pl.video_urls, start=1):
            print(f"Processing video {index} of {len(pl.video_urls)}")
            download_video(video)
                
    if isPlaylist == 'n':
        download_video(url)


if __name__ == "__main__":
    CoreLogic()
