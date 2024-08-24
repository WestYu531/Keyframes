import os
import subprocess

def download_auto_subtitles(video_url, subtitle_lang='en', output_path='/Users/westyu/Desktop/sub'):
    """
    下载指定语言的YouTube视频自动生成的字幕，并保存到指定路径。

    :param video_url: YouTube视频的URL
    :param subtitle_lang: 字幕语言代码，默认为'en'（英语）
    :param output_path: 输出路径，默认为'/Users/westyu/Desktop/sub'
    """
    try:
        # 检查 yt-dlp 是否安装
        subprocess.run(['yt-dlp', '--version'], check=True)
    except subprocess.CalledProcessError:
        print("请先安装 yt-dlp 工具。")
        return
    
    # 构建 yt-dlp 命令
    command = [
        'yt-dlp',
        '--write-auto-sub',      # 下载自动生成的字幕
        '--sub-lang', subtitle_lang, # 指定字幕语言
        '--skip-download',       # 不下载视频
        '-o', os.path.join(output_path, '%(title)s.%(ext)s'), # 指定输出路径
        video_url
    ]

    try:
        # 执行 yt-dlp 命令
        subprocess.run(command, check=True)
        print(f"自动生成的字幕已下载：{video_url}，保存路径：{output_path}")
    except subprocess.CalledProcessError as e:
        print(f"下载字幕时出错: {e}")

if __name__ == "__main__":
    # YouTube视频URL
    video_url = 'https://www.youtube.com/watch?v=fCyFtxa5Rzw'
    # 字幕语言代码（例如：'en' 表示英语）
    subtitle_lang = 'en'
    # 指定输出路径
    output_path = '/Users/westyu/Desktop/sub'

    # 创建输出路径（如果不存在）
    os.makedirs(output_path, exist_ok=True)

    download_auto_subtitles(video_url, subtitle_lang, output_path)
