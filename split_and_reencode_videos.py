import os
import subprocess
import sys

# 检查是否传递了URL作为参数
if len(sys.argv) != 2:
    print("Usage: python split_and_reencode_videos.py <YouTube URL>")
    sys.exit(1)

# 获取YouTube视频的URL
video_url = sys.argv[1]

# 定义源目录和目标目录
SRC_DIR = "/Users/westyu/Desktop/videos"
DEST_DIR = "/Users/westyu/Videos"
SPLIT_DEST_DIR = "/Users/westyu/Desktop/split_videos"
TEMP_FILE = os.path.join(SRC_DIR, "temp_video.mp4")
REENCODED_FILE = os.path.join(SRC_DIR, "reencoded_video.mp4")

# 创建源目录和目标目录（如果不存在）
os.makedirs(SRC_DIR, exist_ok=True)
os.makedirs(DEST_DIR, exist_ok=True)
os.makedirs(SPLIT_DEST_DIR, exist_ok=True)

# 下载视频
yt_dlp_command = [
    "yt-dlp",
    "-o", TEMP_FILE,
    video_url
]

print("Downloading video...")
try:
    subprocess.run(yt_dlp_command, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error occurred while downloading the video: {e}")
    sys.exit(1)

# 重新编码视频
ffmpeg_reencode_command = [
    "ffmpeg",
    "-i", TEMP_FILE,
    "-c:v", "libx264",
    "-c:a", "aac",
    "-strict", "experimental",
    REENCODED_FILE
]

print(f"Reencoding {TEMP_FILE} to {REENCODED_FILE}...")
try:
    subprocess.run(ffmpeg_reencode_command, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error occurred while reencoding the video: {e}")
    sys.exit(1)

# 分段视频（假设每段5分钟）
split_duration = 300  # 分段时长（秒）
split_command = [
    "ffmpeg",
    "-i", REENCODED_FILE,
    "-c", "copy",
    "-map", "0",
    "-segment_time", str(split_duration),
    "-f", "segment",
    "-reset_timestamps", "1",
    os.path.join(SPLIT_DEST_DIR, "myvideo-%03d.mp4")
]

print("Splitting reencoded video...")
try:
    subprocess.run(split_command, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error occurred while splitting the reencoded video: {e}")
    sys.exit(1)

print("The video has been downloaded, reencoded, and split into chapters.")
