import yt_dlp
import argparse
import re
from colorama import just_fix_windows_console
from colorama import Fore, Style

def parse_arguments():
    parser = argparse.ArgumentParser(description="Download a YouTube video or playlist using yt-dlp.")
    parser.add_argument('url', type=str, nargs='?', default=None, help="The YouTube URL (video or playlist)")
    return parser.parse_args()

def print_colored(text, color):
    color_map = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'purple': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE
    }
    print(f"{color_map.get(color, '')}{text}{Style.RESET_ALL}")

def download_with_ytdlp(url):
    def hook(d):
        if d['status'] == 'downloading':
            print_colored(f"↓ {d['_percent_str']} at {d.get('_speed_str', 'unknown')} ETA {d.get('_eta_str', '?')}", "cyan")
        elif d['status'] == 'finished':
            print_colored(f" Finished: {d['filename']}", "green")

    # Output template - safe filename
    outtmpl = "%(title).200s.%(ext)s"

    ydl_opts = {
        'format': 'bv*[vcodec^=avc1][height<=1080]+ba[acodec^=mp4a]/best[ext=mp4]/best',
        'outtmpl': '%(title).200s.%(ext)s',
        'merge_output_format': 'mp4',
        'noplaylist': False,
        'progress_hooks': [hook],
        'sleep_interval': 5,             # Random delay between downloads
        'sleep_interval_requests': 1,   # Delay between individual HTTP requests
        'max_sleep_interval': 10,       # Max delay between downloads (randomized)
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if 'entries' in info:
                print_colored(f"Playlist downloaded: {info.get('title', 'Untitled')}", "purple")
            else:
                print_colored(f"Video downloaded: {info.get('title', 'Untitled')}", "purple")
    except Exception as e:
        print_colored(f"An error occurred: {e}", "red")

def CoreLogic():
    args = parse_arguments()
    url = args.url or input("Please enter the YouTube URL: ").strip()
    download_with_ytdlp(url)

if __name__ == "__main__":
    just_fix_windows_console()
    CoreLogic()
