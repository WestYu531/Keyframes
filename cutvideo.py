import os
import webvtt
import ffmpeg

# 设置文件路径
vtt_file_path = '/Users/westyu/Desktop/sub/1.vtt'  # VTT字幕文件路径
video_file_path = '/Users/westyu/Desktop/videos1/1.mp4'  # 视频文件路径
output_dir = '/Users/westyu/Desktop/subframe'  # 输出的视频片段目录

# 设置关键词
keywords = ['click', 'move', 'select', 'choose']  # 替换为你要提取的关键词

# 前后时间偏移量（秒）
time_offset = 5  # 前后五秒

# 创建输出目录
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 将时间格式从 "HH:MM:SS.sss" 转换为秒数
def time_to_seconds(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

# 将秒数转换回 "HH:MM:SS.sss" 格式
def seconds_to_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:06.3f}"

# 解析VTT文件并提取时间节点信息
clips = []
for caption in webvtt.read(vtt_file_path):
    # 检查字幕文本中是否包含任何关键词
    if any(keyword.lower() in caption.text.lower() for keyword in keywords):
        # 计算截取时间
        start_time = time_to_seconds(caption.start) - time_offset
        end_time = time_to_seconds(caption.end) + time_offset
        
        # 确保时间不会超出视频的开始和结束
        if start_time < 0:
            start_time = 0
        
        clips.append((start_time, end_time))
        print(f"Clip from {seconds_to_time(start_time)} to {seconds_to_time(end_time)}")

# 按时间顺序排序剪辑片段
clips.sort()

# 截取相关视频片段
for i, (start, end) in enumerate(clips):
    start_time_str = seconds_to_time(start).replace(':', '-')
    end_time_str = seconds_to_time(end).replace(':', '-')
    output_file_path = os.path.join(output_dir, f'clip_{i+1}_{start_time_str}_to_{end_time_str}.mp4')
    
    (
        ffmpeg
        .input(video_file_path, ss=seconds_to_time(start), to=seconds_to_time(end))
        .output(output_file_path)
        .run()
    )
    
    # 检查视频片段长度
    probe = ffmpeg.probe(output_file_path)
    duration = float(probe['format']['duration'])
    
    # 如果视频长度小于或等于10秒，删除文件
    if duration < 11:
        os.remove(output_file_path)
        print(f"Clip '{output_file_path}' deleted (duration: {duration:.2f} seconds)")
    else:
        print(f"Clip saved: {output_file_path}")

print("All clips have been successfully processed.")
