"""
BGM快速添加器
功能：给视频快速添加背景音乐
"""

import os
import subprocess
from pathlib import Path

# ============ 配置 ============
FFMPEG = r"C:\Users\52648\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"

# 预设BGM（请替换为你的实际文件路径）
BGM_PRESETS = {
    "electronic": r"C:\Users\52648\Documents\GitHub\ai_xly\bgm\electronic.mp3",
    "upbeat": r"C:\Users\52648\Documents\GitHub\ai_xly\bgm\upbeat.mp3",
    "calm": r"C:\Users\52648\Documents\GitHub\ai_xly\bgm\calm.mp3",
    "fast": r"C:\Users\52648\Documents\GitHub\ai_xly\bgm\fast.mp3",
    "no_lyrics": r"C:\Users\52648\Documents\GitHub\ai_xly\bgm\no_lyrics.mp3",
}


def add_bgm_simple(video_path: str, bgm_path: str, output_path: str = None):
    """
    简单添加BGM（音量0.3，无淡入淡出）

    Args:
        video_path: 视频路径
        bgm_path: BGM路径
        output_path: 输出路径（默认: video_with_bgm_xxx.mp4）
    """
    if output_path is None:
        p = Path(video_path)
        output_path = str(p.parent / f"bgm_{p.name}")

    cmd = [
        FFMPEG, '-y',
        '-i', video_path,
        '-i', bgm_path,
        '-filter_complex', '[0:a]volume=1.0[a1];[1:a]volume=0.3[a2];[a1][a2]amix=inputs=2:duration=longest[aout]',
        '-map', '0:v',
        '-map', '[aout]',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-shortest',
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ BGM已添加: {output_path}")
        return output_path
    else:
        print(f"❌ 错误: {result.stderr}")
        return None


def add_bgm_with_fade(video_path: str, bgm_path: str, output_path: str = None,
                      bgm_volume: float = 0.3, fade_in: float = 1.0, fade_out: float = 1.0):
    """
    添加BGM（带淡入淡出）

    Args:
        video_path: 视频路径
        bgm_path: BGM路径
        bgm_volume: BGM音量 (0.1-1.0)
        fade_in: 淡入时长（秒）
        fade_out: 淡出时长（秒）
    """
    if output_path is None:
        p = Path(video_path)
        output_path = str(p.parent / f"bgm_fade_{p.name}")

    cmd = [
        FFMPEG, '-y',
        '-i', video_path,
        '-i', bgm_path,
        '-filter_complex', f'''
            [0:a]volume=1.0[a1];
            [1:a]volume={bgm_volume}[a2];
            [a1][a2]amix=inputs=2:duration=longest[mix];
            [mix]afade=t=in:st=0:d={fade_in},afade=t=out:T=last:d={fade_out}[aout]
        ''',
        '-map', '0:v',
        '-map', '[aout]',
        '-c:v', 'copy',
        '-c:a', 'aac',
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ BGM已添加（带淡入淡出）: {output_path}")
        return output_path
    else:
        print(f"❌ 错误: {result.stderr}")
        return None


def extract_audio(video_path: str, output_path: str = None):
    """提取视频中的音频"""
    if output_path is None:
        p = Path(video_path)
        output_path = str(p.parent / f"audio_{p.stem}.mp3")

    cmd = [
        FFMPEG, '-y',
        '-i', video_path,
        '-vn',
        '-acodec', 'libmp3lame',
        '-q:a', '2',
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ 音频已提取: {output_path}")
        return output_path
    else:
        print(f"❌ 错误: {result.stderr}")
        return None


def get_audio_info(audio_path: str) -> dict:
    """获取音频信息"""
    cmd = [
        FFMPEG, '-i', audio_path,
        '-f', 'null',
        '-'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, input="q"
    )

    # 解析时长
    import re
    match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2})", result.stderr)
    if match:
        h, m, s = match.groups()
        duration = int(h) * 3600 + int(m) * 60 + int(s)
        return {"duration": duration}

    return None


# ============ 快速使用 ============
if __name__ == "__main__":
    import sys

    video = r"C:\Users\52648\Documents\GitHub\ai_xly\outputs\ali_qwen_hot_video_full.mp4"

    print("=" * 60)
    print("BGM快速添加器")
    print("=" * 60)

    # 检查视频是否存在
    if not os.path.exists(video):
        print(f"❌ 视频不存在: {video}")
        sys.exit(1)

    # 方案1：使用预设BGM
    print("\n可用预设BGM:")
    for name, path in BGM_PRESETS.items():
        status = "✅" if os.path.exists(path) else "❌"
        print(f"  {status} {name}: {os.path.basename(path) if os.path.exists(path) else '文件不存在'}")

    print("\n使用方法:")
    print("python bgm_adder.py electronic    # 添加电子音乐")
    print("python bgm_adder.py upbeat       # 添加激励音乐")
    print("python bgm_adder.py calm        # 添加舒缓音乐")
    print("python bgm_adder.py fast        # 添加快节奏音乐")
    print("python bgm_adder.py no_lyrics  # 添加无歌词音乐")

    # 如果有参数，执行
    if len(sys.argv) > 1:
        style = sys.argv[1]
        if style in BGM_PRESETS:
            bgm_path = BGM_PRESETS[style]
            if os.path.exists(bgm_path):
                output = video.replace(".mp4", f"_{style}.mp4")
                add_bgm_with_fade(video, bgm_path, output)
            else:
                print(f"\n⚠️ BGM文件不存在: {bgm_path}")
                print("\n请选择其他方案:")
                print("1. 将你的BGM文件放到 bgm/ 目录")
                print("2. 修改 BGM_PRESETS 中的路径")
        else:
            print(f"❌ 未知的BGM类型: {style}")

    else:
        # 默认使用electronic（如果存在）
        if "electronic" in BGM_PRESETS and os.path.exists(BGM_PRESETS["electronic"]):
            bgm_path = BGM_PRESETS["electronic"]
            output = video.replace(".mp4", "_bgm.mp4")
            add_bgm_with_fade(video, bgm_path, output)
        else:
            print("\n⚠️ 未找到预设BGM")
            print("请执行: python bgm_adder.py <BGM类型>")
