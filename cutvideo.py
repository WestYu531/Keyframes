import os
import webvtt
import ffmpeg

# 设置文件夹路径
vtt_folder_path = '/Users/westyu/Desktop/sub/'  # VTT字幕文件夹路径
video_folder_path = '/Users/westyu/Desktop/videos1/'  # 视频文件夹路径
output_root_dir = '/Users/westyu/Desktop/subframe/'  # 所有输出的视频片段的根目录

# 设置关键词
keywords = ['click', 'move', 'select', 'choose']  # 替换为你要提取的关键词

# 前后时间偏移量（秒）
time_offset = 5  # 前后五秒

# 创建根输出目录
if not os.path.exists(output_root_dir):
    os.makedirs(output_root_dir)

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

# 获取VTT文件列表
vtt_files = [f for f in os.listdir(vtt_folder_path) if f.endswith('.vtt')]

# 处理每个VTT文件及其对应的视频文件
for vtt_file in vtt_files:
    video_file_name = os.path.splitext(vtt_file)[0] + '.mp4'
    vtt_file_path = os.path.join(vtt_folder_path, vtt_file)
    video_file_path = os.path.join(video_folder_path, video_file_name)
    
    if not os.path.exists(video_file_path):
        print(f"Video file '{video_file_name}' not found. Skipping...")
        continue
    
    # 为当前视频创建一个专属的输出子目录
    video_output_dir = os.path.join(output_root_dir, os.path.splitext(video_file_name)[0])
    if not os.path.exists(video_output_dir):
        os.makedirs(video_output_dir)
    
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
            print(f"Clip from {seconds_to_time(start_time)} to {seconds_to_time(end_time)} for file '{video_file_name}'")
    
    # 按时间顺序排序剪辑片段
    clips.sort()

    # 截取相关视频片段
    for i, (start, end) in enumerate(clips):
        start_time_str = seconds_to_time(start).replace(':', '-')
        end_time_str = seconds_to_time(end).replace(':', '-')
        output_file_name = f'clip_{i+1}_{start_time_str}_to_{end_time_str}.mp4'
        output_file_path = os.path.join(video_output_dir, output_file_name)
        
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

print("All files have been successfully processed.")
