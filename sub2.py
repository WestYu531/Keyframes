import re
import os
import cv2
from Katna.video import Video
from Katna.writer import KeyFrameDiskWriter

def extract_timestamps_from_txt(txt_file, keywords):
    """从 TXT 文件中提取包含关键词的时间节点"""
    with open(txt_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 正则表达式匹配时间戳和对应的字幕文本
    pattern = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\s+([^\n]+)')
    matches = pattern.findall(content)
    
    results = []
    
    for start_time, end_time, text in matches:
        for keyword in keywords:
            if keyword.lower() in text.lower():  # 忽略大小写
                results.append((start_time, end_time, text))
                break
    
    return results

def time_to_frame(time_str, fps):
    """将时间格式转换为视频帧数"""
    h, m, s = time_str.split(':')
    s, ms = map(float, s.split('.'))
    total_seconds = int(h) * 3600 + int(m) * 30 + s + ms / 1000.0
    return int(total_seconds * fps)

def extract_keyframes_at_timestamps(video_file_path, timestamps, output_dir):
    """根据时间节点提取关键帧并保存"""
    vd = Video()
    
    cap = cv2.VideoCapture(video_file_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video file {video_file_path}")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    # 计算要提取的关键帧数量，等于时间节点数量的三倍
    no_of_frames_to_extract = 3

    diskwriter = KeyFrameDiskWriter(location=output_dir)

    for start_time, end_time, _ in timestamps:
        start_frame = time_to_frame(start_time, fps)
        end_frame = time_to_frame(end_time, fps)
        
        print(f"Extracting {no_of_frames_to_extract} frames from {start_time} to {end_time} (Frames {start_frame} to {end_frame})")

        vd.extract_video_keyframes(
            no_of_frames=no_of_frames_to_extract,
            file_path=video_file_path,
            writer=diskwriter
        )
        
if __name__ == "__main__":
    # 配置部分
    txt_file = '/Users/westyu/Desktop/sub4/1.txt'  # TXT 文件路径
    video_file_path = '/Users/westyu/Desktop/videos1/1.mp4'  # 视频文件路径，使用绝对路径
    keywords = ['click', 'move', 'select', 'choose']  # 关键词列表
    output_dir = "/Users/westyu/Desktop/subframe"  # 关键帧保存目录
    
    # 1. 提取时间节点
    timestamps = extract_timestamps_from_txt(txt_file, keywords)
    
    if not timestamps:
        print("No matching timestamps found.")
    else:
        print("Extracted timestamps:")
        for start_time, end_time, text in timestamps:
            print(f"Start: {start_time}, End: {end_time}, Text: {text}")
        
        # 2. 提取关键帧
        extract_keyframes_at_timestamps(video_file_path, timestamps, output_dir)
