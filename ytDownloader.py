from pytubefix import Playlist, YouTube
from pytubefix.cli import on_progress
import re  # Import the 're' module for regular expressions
import os
import subprocess

def download_video():
    # Ask the user to provide the YouTube video URL
    url = input("Please enter the YouTube video URL: ")
     
    pl = Playlist(url)
    for video in pl:
        try:
            # Create a YouTube object
            yt = YouTube(video, on_progress_callback=on_progress)

            # Display the video title
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

                # Download the video and audio streams
                video_path = video_stream.download(filename="video.mp4")
                print(f"Video stream downloaded: {video_path}")
                audio_path = audio_stream.download(filename="audio.mp4")
                print(f"Audio stream downloaded: {audio_path}")

                # Combine the video and audio streams with ffmpeg
                output_path = f"{re.sub(r'[\\/*?:"<>|]', '', yt.title)}.mp4"
                subprocess.run([
                    'ffmpeg',
                    '-i', video_path,
                    '-i', audio_path,
                    '-c:v', 'copy',
                    '-c:a', 'aac',
                    '-strict', 'experimental',
                    output_path
                ])
                print(f"Combined video saved: {output_path}")

                # Clean up temporary files
                os.remove(video_path)
                os.remove(audio_path)
                
                #sanitized_title = re.sub(r'[\\/*?:"<>|]', '', yt.title)  # Remove illegal characters
                #new_output_path = f"{sanitized_title}.mp4"
                #os.rename(output_path, new_output_path)

                print("Download and combination completed!")
            else:
                # Download the progressive stream
                # video_stream.download(filename="final_video.mp4")
                video_stream.download()
                print("Download completed!")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_video()
