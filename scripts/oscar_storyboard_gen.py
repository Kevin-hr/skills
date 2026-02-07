#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
奥斯卡级别分镜图生成器
支持 9:16 和 16:9 两种规格
"""

import json
import os
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

# 配置
OUTPUT_DIR = Path(__file__).parent / "outputs" / "storyboards"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 规格定义
FORMATS = {
    "9:16": {"width": 1080, "height": 1920},
    "16:9": {"width": 1920, "height": 1080}
}

# DeepSeek 6场景完整版 (73秒)
SCENES_16X9 = [
    {
        "id": "01",
        "duration": 3,
        "title": "开场钩子 - 悬念建立",
        "hook": "别再用传统方式了！",
        "subtitle": "这个 DeepSeek 免费还更强",
        "visual_style": "电影质感",
        "color_scheme": ["#0a0a1a", "#1a1a3a"],
        "accent": "#00D4FF",
        "shot_scale": "ELS",
        "camera_move": "推进"
    },
    {
        "id": "02",
        "duration": 8,
        "title": "痛点场景 - 情绪低谷",
        "hook": "曾经的我们",
        "subtitle": "效率低，还费钱",
        "visual_style": "真实写实",
        "color_scheme": ["#1a1a1a", "#2a2a2a"],
        "accent": "#666666",
        "shot_scale": "LS",
        "camera_move": "静态"
    },
    {
        "id": "03",
        "duration": 15,
        "title": "转折点 - 揭示方案",
        "hook": "直到我遇见了它",
        "subtitle": "DeepSeek - 国产AI之光",
        "visual_style": "赛博朋克",
        "color_scheme": ["#0a0a2a", "#1a0a3a"],
        "accent": "#7B2FFF",
        "shot_scale": "MS",
        "camera_move": "滑轨横移"
    },
    {
        "id": "04",
        "duration": 25,
        "title": "核心展示 - 功能演示",
        "hook": "三步搞定",
        "subtitle": "输入 → 理解 → 输出",
        "visual_style": "屏幕录制",
        "color_scheme": ["#0a1a2a", "#0f2a4a"],
        "accent": "#00D4FF",
        "shot_scale": "特写",
        "camera_move": "平滑移动"
    },
    {
        "id": "05",
        "duration": 15,
        "title": "效果对比 - 视觉冲击",
        "hook": "差距，一目了然",
        "subtitle": "左边 → 右边 | 3分钟 vs 1小时",
        "visual_style": "分屏对比",
        "color_scheme": ["#1a2a1a", "#2a1a1a"],
        "accent": "#00FF87",
        "shot_scale": "中特写",
        "camera_move": "静态"
    },
    {
        "id": "06",
        "duration": 7,
        "title": "总结升华 - 行动号召",
        "hook": "未来已经来了",
        "subtitle": "评论区扣【1】领使用指南",
        "visual_style": "电影质感",
        "color_scheme": ["#1a2a3a", "#2a4a6a"],
        "accent": "#FFD700",
        "shot_scale": "MS",
        "camera_move": "拉远"
    }
]


def load_font(size):
    """加载字体"""
    font_paths = [
        "msyh.ttc",
        "msyhbd.ttc",
        "simhei.ttf",
        "simsun.ttc",
        "C:/Windows/Fonts/msyh.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc"
    ]
    for fp in font_paths:
        try:
            return ImageFont.truetype(fp, size)
        except:
            continue
    return ImageFont.load_default()


def create_bg(width, height, colors):
    """创建渐变背景"""
    base = Image.new('RGB', (width, height), colors[0])
    for y in range(height):
        ratio = y / height
        r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
        g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
        b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
        for x in range(width):
            base.putpixel((x, y), (r, g, b))
    return base


def hex_to_rgb(hex_color):
    """HEX转RGB"""
    hex_color = str(hex_color).lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def draw_centered_text(draw, text, y, font, color, width):
    """居中绘制文字"""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (width - text_w) // 2
    draw.text((x, y), text, font=font, fill=color)
    return y + (bbox[3] - bbox[1]) + 20


def generate_scene_image(scene, format_key, output_dir):
    """生成单个场景图"""
    fmt = FORMATS[format_key]
    width = fmt["width"]
    height = fmt["height"]
    colors = [hex_to_rgb(c) for c in scene["color_scheme"]]

    # 创建背景
    img = create_bg(width, height, colors)
    draw = ImageDraw.Draw(img)

    # 加载字体
    try:
        if format_key == "9:16":
            font_title = ImageFont.truetype("msyhbd.ttc", 72)
            font_subtitle = ImageFont.truetype("msyh.ttc", 52)
            font_small = ImageFont.truetype("msyh.ttc", 36)
            font_accent = ImageFont.truetype("msyhbd.ttc", 80)
        else:
            font_title = ImageFont.truetype("msyhbd.ttc", 56)
            font_subtitle = ImageFont.truetype("msyh.ttc", 40)
            font_small = ImageFont.truetype("msyh.ttc", 28)
            font_accent = ImageFont.truetype("msyhbd.ttc", 64)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_accent = ImageFont.load_default()

    accent_rgb = hex_to_rgb(scene["accent"])

    # 左上角：场景信息
    draw.rectangle([(30, 30), (300, 100)], fill=(0, 0, 0, 150))
    draw.text((50, 45), f"场景 {scene['id']}/06", font=font_small, fill=(200, 200, 200))

    # 右上角：时长
    draw.rectangle([(width - 200, 30), (width - 50, 100)], fill=(0, 0, 0, 150))
    draw.text((width - 180, 45), f"{scene['duration']}秒", font=font_small, fill=(accent_rgb[0], accent_rgb[1], accent_rgb[2]))

    # 中央：主标题（大字）
    center_y = height // 2 - 100
    draw_centered_text(draw, scene["hook"], center_y, font_accent, accent_rgb, width)

    # 副标题
    subtitle_y = center_y + 120
    draw_centered_text(draw, scene["subtitle"], subtitle_y, font_subtitle, (255, 255, 255), width)

    # 底部：风格标签
    bottom_y = height - 180
    style_text = f"{scene['visual_style']} | {scene['shot_scale']} | {scene['camera_move']}"
    draw_centered_text(draw, style_text, bottom_y, font_small, (150, 150, 150), width)

    # 标题栏
    title_y = height // 2 - 220
    draw.rectangle([(0, title_y), (width, title_y + 2)], fill=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 180))

    # 装饰光效
    for _ in range(15):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(2, 6)
        alpha = random.randint(30, 80)
        draw.ellipse(
            [(x - r, y - r), (x + r, y + r)],
            fill=(accent_rgb[0], accent_rgb[1], accent_rgb[2], alpha)
        )

    # 保存
    filename = f"scene_{scene['id']}_{format_key.replace(':', 'x')}.png"
    filepath = output_dir / filename
    img.save(filepath, "PNG", quality=95)
    print(f"  [OK] {filename}")

    return str(filepath)


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("奥斯卡级别分镜图生成器")
    print("主题: DeepSeek AI工具横评")
    print("=" * 60)

    results = {
        "16x9": [],
        "9x16": []
    }

    # 生成16:9版本
    print("\n[16:9 横版]")
    output_16x9 = OUTPUT_DIR / "oscar_16x9"
    output_16x9.mkdir(parents=True, exist_ok=True)

    for scene in SCENES_16X9:
        path = generate_scene_image(scene, "16:9", output_16x9)
        results["16x9"].append({
            "scene_id": scene["id"],
            "output_path": path,
            "duration": scene["duration"],
            "hook": scene["hook"],
            "visual_style": scene["visual_style"]
        })

    # 生成9:16版本
    print("\n[9:16 竖版]")
    output_9x16 = OUTPUT_DIR / "oscar_9x16"
    output_9x16.mkdir(parents=True, exist_ok=True)

    for scene in SCENES_16X9:
        path = generate_scene_image(scene, "9:16", output_9x16)
        results["9x16"].append({
            "scene_id": scene["id"],
            "output_path": path,
            "duration": scene["duration"],
            "hook": scene["hook"],
            "visual_style": scene["visual_style"]
        })

    # 保存结果
    result_file = OUTPUT_DIR / "oscar_scenes_result.json"
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("分镜图生成完成！")
    print(f"结果文件: {result_file}")
    print("=" * 60)

    # 生成FFmpeg concat文件
    for fmt, scenes in results.items():
        concat_file = OUTPUT_DIR / f"oscar_{fmt.replace('x', 'x')}_concat.txt"
        with open(concat_file, "w", encoding="utf-8") as f:
            for scene in scenes:
                f.write(f"file '{scene['output_path']}'\n")
                f.write(f"duration {scene['duration']}\n")
            # 最后一张重复
            f.write(f"file '{scenes[-1]['output_path']}'\n")
        print(f"Concat文件: {concat_file}")

    return results


if __name__ == "__main__":
    main()
