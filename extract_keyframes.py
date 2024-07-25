import os
import sys
import cv2

def extract_keyframes_every_n_seconds(video_file_path, output_dir, interval_seconds):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 打开视频文件
    cap = cv2.VideoCapture(video_file_path)
    if not cap.isOpened():
        print(f"无法打开视频文件: {video_file_path}")
        return

    # 获取视频的帧率和总帧数
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    print(f"视频总帧数: {total_frames}, 帧率: {fps}, 总时长: {duration} 秒")

    # 计算每隔 interval_seconds 秒提取的帧号
    frame_indices = [int(i * fps) for i in range(0, int(duration), interval_seconds)]
    print(f"将提取以下帧号: {frame_indices}")

    # 按帧号提取关键帧
    keyframes = []
    for frame_idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if ret:
            keyframes.append(frame)
        else:
            print(f"无法读取帧号: {frame_idx}")

    cap.release()

    # 将关键帧保存到指定位置
    for idx, frame in enumerate(keyframes):
        frame_path = os.path.join(output_dir, f"keyframe_{idx + 1}.jpg")
        cv2.imwrite(frame_path, frame)

    print(f"关键帧提取完成并保存到 {output_dir} 目录中")

if __name__ == "__main__":
    # 检查是否传递了视频文件目录和输出目录作为参数
    if len(sys.argv) != 3:
        print("Usage: python extract_keyframes.py <video_files_directory> <output_directory>")
        sys.exit(1)

    # 视频文件目录
    video_files_dir = sys.argv[1]

    # 输出主目录
    main_output_dir = sys.argv[2]

    # 提取间隔（秒）
    interval_seconds = 3

    # 确保输出主目录存在
    os.makedirs(main_output_dir, exist_ok=True)

    # 遍历视频文件目录中的所有视频文件
    for video_filename in os.listdir(video_files_dir):
        if video_filename.endswith(".mp4"):
            video_file_path = os.path.join(video_files_dir, video_filename)
            output_dir = os.path.join(main_output_dir, os.path.splitext(video_filename)[0])

            print(f"处理视频文件: {video_file_path}")

            # 提取关键帧并保存
            extract_keyframes_every_n_seconds(video_file_path, output_dir, interval_seconds)
