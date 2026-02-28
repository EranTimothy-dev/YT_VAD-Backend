import threading
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from app.services.ExtractionOptions import getThumbnail, extract_video_info, extract_playlist_info, get_available_quality
from app.services.DownloadOptions import download_video, download_age_restricted_video, download_audio
import threading
import time
from app.services.downloadHandler import get_information, convert_image_to_base64

playlist_url = "https://youtube.com/playlist?list=PLbpi6ZahtOH7c6nDA9YG3QcyRGbZ4xDFn&si=TClA3jkK99Ce2DRl"
url = "https://youtu.be/Js6H70-eADY?si=fF6a5sRPprlb1MDr"
thumbnail_filepath = "thumbnail\\"
url1 = "https://youtu.be/whEObh8waxg?si=kBbfH05WMNQpNTvJ"
url2 = "https://youtu.be/_kkvcijCQ38?si=iE1zlTnG6cl0Mjpz"
age_restricted_video = "https://youtu.be/voQBX6yn2XY?si=e_4DHuE3jUDv5whc"


# make a thread class with return value
class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, *, daemon=None,
                 verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return


# input_url = input("Enter youtube video url: ")
# getThumbnail(input_url,thumbnail_filepath)
# image_bytecode = convert_image_to_base64()
# print(image_bytecode)
# vid_info = get_information(input_url)
# print(vid_info.video_info.title)
# print(vid_info.available_resolutions)

input_url2 = input("Enter youtube video url: ")
availbale_quality = get_available_quality(input_url2)
available_extensions = {"mp4","webm","mkv"}
print("available extensions: ",available_extensions)
# print(availbale_quality)
print("available quality: ")
for count,quality in enumerate(availbale_quality,1):
    print(f"{count}. {quality[0]}x{quality[1]}")    

quality = input("Enter video quality: ")
extension = input("Enter video extension: ")
t1 = ThreadWithReturnValue(target=download_video, args=(input_url2,quality,extension,))
# t1 = ThreadWithReturnValue(target=download_audio, args=(input_url,))
# t1 = ThreadWithReturnValue(target=extract_video_info, args=(input_url2,))
# t1 = ThreadWithReturnValue(target=extract_playlist_info, args=(input_url2,))
# t2 = ThreadWithReturnValue(target=extract_video_info, args=(input_url2,))
# t2.start()
# time.sleep(1)
# t1._stop()
t1.start()
# info, pl = t1.join()
info = t1.join()
# info2 = t2.join()
# for line in pl.stdout:
    # print(f"\r{line.strip():<150}", end="",flush=True) # make sure the progress is printied on the same line
    # print(line.strip())
    # print(line)
    # print(info2.stdout)
print("\n\n")

for line in info.stdout:
    print(f"\r{line.strip():<150}", end="",flush=True) # make sure the progress is printied on the same line
    # print(line.strip())
    # print(info2.stdout)

# for line in info2.stdout:
#     # print(f"\r{line.strip():<150}", end="",flush=True) # make sure the progress is printied on the same line
#     print(line.strip())
#     # print(info2.stdout)

import re

# Example string
text = "'%(title)s': '#1 Connecting to Postgres with SQLAlchemy & Docker | FastAPI JWT Authorization and Authentication'"

# Regex pattern
pattern = r"'%\((\w+)\)s': ['\"](.*)['\"]"


# def print1(info, number):
#     for line in info.stdout:
#         # print(f"this is the {number} thread")
#         # print(line.strip())
#         match = re.search(pattern, line.strip())  # match() checks from the beginning of the string
#         if match:
#             # print("Pattern matched!")
#             print(f"{match.groups()[0]} : {match.groups()[1]}")
#         else:
#             # print("No match.")
#             continue

# t3 = ThreadWithReturnValue(target=print1, args=(info,1))
# # t4 = ThreadWithReturnValue(target=print1, args=(info2,2))
# t3.start()
# # t4.start()
# t3.join()
# # t4.join()




# t1 = ThreadWithReturnValue(target=extract_video_info, args=(playlist_url,))
# t1 = ThreadWithReturnValue(target=download_age_restricted_video, args=(age_restricted_video,))
# t2 = ThreadWithReturnValue(target=extract_playlist_info, args=(playlist_url,))
# t2.start()
# video_info, playlist_info = t2.join() 
# print(type(playlist_info))
# print(playlist_info)
# print("\n\n")
# print(video_info)


# print(info)


# for line in video_info.stdout:
#     print(line.strip())
# import subprocess

# def is_firefox_installed():
#     cmd = 'firefox --version'
#     p = subprocess.Popen(['firefox','--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout, stderr = p.communicate()

# is_firefox_installed()
        

# print("\n\n")
# print(playlist_info)
# check video information extractor for playlists
# video_extractor_thread = ThreadWithReturnValue(target=get_video_info, args=(playlist_url,))
# video_extractor_thread.start()
# video_info, video_uploader, video_views, video_likes = video_extractor_thread.join()
# video_info, video_uploader, video_views, video_likes = get_video_info(playlist_url)

# def get_video_info(url):
#     # get the video information
#     # Set up yt-dlp options
#     ydl_opts = {
#         'quiet': True,  # Suppress output
#         # 'noplaylist': True,  # Do not download playlists
#         'yesplaylist': True,  
#     }

#     # Create a YoutubeDL instance with the options
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         # Extract info from the URL
#         info_dict = ydl.extract_info(url, download=False)  # Set download to False to only get metadata

#         # Extract desired information
#         video_title = info_dict.get('title', 'Unknown Title')
#         uploader = info_dict.get('uploader', 'Unknown Uploader')
#         view_count = info_dict.get('view_count', 'Unknown Views')
#         like_count = info_dict.get('like_count', 'Unknown Likes')

#         # Print the extracted information
#         # print(f'Title: {video_title}')
#         # print(f'Uploader: {uploader}')
#         # print(f'Views: {view_count}')
#         # print(f'Likes: {like_count}')

#         return video_title,uploader,view_count,like_count