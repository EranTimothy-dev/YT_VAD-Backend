import subprocess
# from subprocess import CREATE_NEW_PROCESS_GROUP


def download_audio(url):
    cmd = ['yt-dlp', url, "--extract-audio", "--audio-format", "mp3", "-P", "downloads\\", "-P", "temp:temp\\","--windows-filenames"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, universal_newlines=True, bufsize=1, encoding="utf-8", start_new_session=True)
    return process
    # subprocess.run(cmd, capture_output=True, text = True)


def download_video(url,quality,extension):
    cmd = ['yt-dlp', url,"-f", f"bv*[height={quality}]+ba","--merge-output-format", f"{extension}", "-P", "downloads\\", "-P", "temp:temp\\","--windows-filenames","-N", "4"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, universal_newlines=True, bufsize=1, encoding="utf-8", start_new_session=True)
    return process
    # subprocess.run(cmd, text = True, check=True)

def download_age_restricted_video(url, quality, extension, browser):
    cmd = ['yt-dlp',"--cookies-from-browser", f"{browser}", url,"-f", f"bv*[height={quality}]+ba","--merge-output-format", f"{extension}", "-P", "downloads\\", "-P", "temp:temp\\","--windows-filenames","-N", "4"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, universal_newlines=True, bufsize=1, encoding="utf-8", start_new_session=True)
    return process
    







