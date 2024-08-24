from Katna.video import Video
from Katna.writer import KeyFrameDiskWriter
import os

def extract_keyframes_recursive(input_dir, output_dir, no_of_frames):
    """
    递归处理输入目录中的所有视频，提取关键帧并保存到对应的输出目录中。

    参数:
    - input_dir: 包含视频文件和子文件夹的主目录路径
    - output_dir: 保存关键帧的主目录路径
    - no_of_frames: 每个视频中需要提取的关键帧数量
    """
    # 初始化视频模块
    vd = Video()

    # 遍历输入目录中的所有文件和文件夹
    for root, dirs, files in os.walk(input_dir):
        # 计算当前路径的相对路径
        relative_path = os.path.relpath(root, input_dir)

        # 创建对应的输出文件夹路径
        output_subdir = os.path.join(output_dir, relative_path)
        if not os.path.exists(output_subdir):
            os.makedirs(output_subdir)

        # 初始化DiskWriter以保存关键帧
        diskwriter = KeyFrameDiskWriter(location=output_subdir)

        # 处理当前文件夹中的所有视频文件
        video_files = [f for f in files if f.endswith(('.mp4', '.mov'))]
        for video_file in video_files:
            video_file_path = os.path.join(root, video_file)
            print(f"Processing video: {video_file_path}")

            # 提取关键帧并保存
            vd.extract_video_keyframes(
                no_of_frames=no_of_frames, file_path=video_file_path,
                writer=diskwriter
            )

    print(f"All keyframes saved to {output_dir}")

if __name__ == "__main__":
    # 输入主目录路径
    input_directory = "/Users/westyu/Desktop/subframe"  # 替换为包含视频文件和子文件夹的主目录路径

    # 输出主目录路径
    output_directory = "/Users/westyu/Desktop/subkeyframe"  # 替换为保存关键帧的主目录路径

    # 提取的关键帧数量
    number_of_frames_to_extract = 4

    # 调用函数递归处理文件夹中的视频
    extract_keyframes_recursive(input_directory, output_directory, number_of_frames_to_extract)
