from pytubefix import Playlist, YouTube
from pytubefix.cli import on_progress
import re  # Import the 're' module for regular expressions
import os
import subprocess
import argparse
from colorama import just_fix_windows_console

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process a YouTube URL for downloading videos.")
    parser.add_argument('url', type=str, nargs='?', default=None, help="The YouTube URL (optional)")    
    return parser.parse_args()

def print_colored(text, color):
    colors = {
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'purple': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m'  # Reset to default color
    }
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

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
        print_colored(f"Combined video saved: {output_path}", "green")
    except subprocess.CalledProcessError:
        print_colored("FFmpeg failed to combine audio and video. Please ensure it is installed.", "red")
    finally:
        os.remove(video_path)
        os.remove(audio_path)

def download_video(video):
    try:
        # Create a YouTube object
        # yt = YouTube(video, 'WEB', on_progress_callback=on_progress)  # use_po_token=True
        yt = YouTube(video, on_progress_callback=on_progress)
        print_colored(f"Downloading video: {yt.title}", "green")

        # Get the stream with the highest resolution (may be adaptive)
        video_stream = yt.streams.get_highest_resolution(False)
        print_colored(f"Selected video stream: {video_stream.resolution} ({video_stream.fps}fps)", "yellow")

        # Check if the stream is adaptive
        if not video_stream.is_progressive:
            # Get the audio stream with the best quality
            audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            print_colored(f"Selected audio stream: {audio_stream.abr}", "yellow")

            if not audio_stream:
                raise Exception('No suitable audio stream found.')
            
            video_name = f"video_{yt.title}.mp4"
            audio_name = f"audio_{yt.title}.mp4"
            
            # Download the video and audio streams
            video_path = video_stream.download(filename=video_name)
            print_colored(f"Video stream downloaded: {video_path}", "purple")
            audio_path = audio_stream.download(filename=audio_name)
            print_colored(f"Audio stream downloaded: {audio_path}", "purple")
            
            output_path = f"{re.sub(r'[\\/*?:"<>|]', '', yt.title)}.mp4"
            combine_streams(video_path, audio_path, output_path)
        else:
            video_stream.download()
            print_colored("Download completed!", "green")
    except Exception as e:
        print_colored(f"An error occurred: {e}", "red")


def CoreLogic():
    
    # isPlaylist = 0
        # while isPlaylist not in {'y', 'n'}:
            # isPlaylist = input("Type Y/y or N/n if it's a playlist: ").strip().lower()    
    
    args = parse_arguments()  # Parse the command-line arguments
    if not args.url:
        url = input("Please enter the YouTube URL: ")
    else:
        print_colored(f"URL provided: {args.url}", "yellow")
        url = args.url
    
    # if isPlaylist == 'y':
    if "list" in url:
        pl = Playlist(url)
        for index, video in enumerate(pl.video_urls, start=1):
            text = f"Processing video {index} of {len(pl.video_urls)}"
            print_colored(text, 'cyan')
            #print(f"Processing video {index} of {len(pl.video_urls)}")
            download_video(video)
    elif "list" not in url:         
    # if isPlaylist == 'n':
        download_video(url)
    else:
        print_colored(f"{url} How?!", "red")

if __name__ == "__main__":
    just_fix_windows_console() #it’s safe to call this function on non-Windows platforms
    CoreLogic()
