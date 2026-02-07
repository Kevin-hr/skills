#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FLUX-Klein 9宫格分镜生成器
基于焦点接力机制 + 9镜头流体结构

遵循标准:
- 奥斯卡级别五维结构
- FLUX-Klein工作流规范
- 9镜头通用流体结构

作者: Claude Code
日期: 2026-02-07
"""

import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
from datetime import datetime


class ToneType(Enum):
    """图像调性类型"""
    TRANQUIL = "静谧/情感"      # 类型A: 温馨、治愈、悲伤
    SUSPENSE = "悬疑/探索"       # 类型B: 神秘、紧张、发现
    INTENSE = "激烈/战斗"        # 类型C: 动作、打斗、速度


class ShotType(Enum):
    """镜头类型"""
    ELS = "全景"      # Extreme Long Shot
    LS = "远景"       # Long Shot
    MS = "中景"       # Medium Shot
    CU = "特写"       # Close-Up
    ECU = "极近特写"  # Extreme Close-Up


class CameraMovement(Enum):
    """运镜方式"""
    PUSH = "推进"
    PULL = "拉远"
    PAN = "横移"
    TILT = "升降"
    ORBIT = "环绕"
    STATIC = "静止"


class Transition(Enum):
    """转场方式"""
    CUT = "cut"
    DISSOLVE = "dissolve"
    WIPE = "wipe"
    MATCH_CUT = "match_cut"


@dataclass
class ShotConfig:
    """单个镜头配置"""
    shot_num: int
    shot_type: str           # 镜头类型: 全景/远景/中景/特写/极近特写
    camera_move: str         # 运镜方式
    description: str         # 画面描述
    tone: str                # 调性
    focus_relay: str = ""    # 焦点接力说明
    duration: float = 8.0    # 时长(秒)


@dataclass
class VisualAnchor:
    """视觉锚点"""
    name: str                # 主体名称
    description: str         # 详细描述
    key_feature: str        # 关键特征


@dataclass
class FluxKleinStoryboard:
    """完整9宫格分镜"""
    board_id: str
    topic: str
    visual_anchor: Dict
    tone_type: str
    shots: List[Dict]
    format: str
    created_at: str = ""

    def to_dict(self) -> Dict:
        return {
            "board_id": self.board_id,
            "topic": self.topic,
            "visual_anchor": self.visual_anchor,
            "tone_type": self.tone_type,
            "shots": self.shots,
            "format": self.format,
            "created_at": self.created_at or datetime.now().isoformat()
        }


class FluxKleinStoryboardGenerator:
    """
    FLUX-Klein 9宫格分镜生成器

    核心机制:
    1. 焦点接力 (Focus Relay) - 实现流水般叙事
    2. 9镜头通用流体结构 - 严格的镜头焦点转移逻辑
    3. 图像调性自适应 - 根据类型选择衔接方式
    """

    # 调性对应的衔接方式
    TONE_ADAPTATION = {
        ToneType.TRANQUIL: {
            "connector": "光影变化",
            "visual_cue": "微表情、眼泪、风吹草动",
            "motion": "轻柔、缓慢、流动"
        },
        ToneType.SUSPENSE: {
            "connector": "脚步移动",
            "visual_cue": "手部触碰、手电筒光束、门的开合",
            "motion": "渐进、谨慎、试探"
        },
        ToneType.INTENSE: {
            "connector": "速度线",
            "visual_cue": "碰撞、碎片、物理位移",
            "motion": "快速、猛烈、冲击"
        }
    }

    # 9镜头流体结构模板
    FLUID_STRUCTURE = [
        {
            "stage": "全景入画",
            "shot_type": "ELS",
            "camera_move": "STATIC",
            "focus": "大环境",
            "objective": "Visual Anchor处于环境中",
            "duration": 8
        },
        {
            "stage": "推进/聚焦",
            "shot_type": "MS",
            "camera_move": "PUSH",
            "focus": "Visual Anchor局部",
            "objective": "聚焦眼睛/手/配饰",
            "duration": 6
        },
        {
            "stage": "触发/诱因",
            "shot_type": "CU",
            "camera_move": "STATIC",
            "focus": "环境微小变化",
            "objective": "引起Visual Anchor注意",
            "duration": 6
        },
        {
            "stage": "反应/互动",
            "shot_type": "MS",
            "camera_move": "PAN",
            "focus": "Visual Anchor反应",
            "objective": "转头/伸手/起步/眼神流转",
            "duration": 8
        },
        {
            "stage": "过程/流动",
            "shot_type": "LS",
            "camera_move": "ORBIT",
            "focus": "动作进行时",
            "objective": "行走/奔跑/抚摸/哭泣",
            "duration": 10
        },
        {
            "stage": "高点/特写",
            "shot_type": "ECU",
            "camera_move": "PUSH",
            "focus": "关键瞬间",
            "objective": "手指触碰/泪水滴落/全力冲刺",
            "duration": 8
        },
        {
            "stage": "变化/后果",
            "shot_type": "CU",
            "camera_move": "STATIC",
            "focus": "环境反馈",
            "objective": "物体亮起/花瓣散开/门打开",
            "duration": 6
        },
        {
            "stage": "余韵/局部",
            "shot_type": "ECU",
            "camera_move": "PULL",
            "focus": "变化细节",
            "objective": "发光纹路/水渍/羽毛",
            "duration": 6
        },
        {
            "stage": "拉远/出画",
            "shot_type": "ELS",
            "camera_move": "PULL",
            "focus": "整体环境",
            "objective": "与环境融为一体或离开",
            "duration": 8
        }
    ]

    def __init__(self):
        self.board_id = f"flux_klein_{int(time.time())}"

    def generate(
        self,
        topic: str,
        visual_anchor: Dict,
        tone_type: str = "静谧/情感",
        format: str = "9:16"
    ) -> FluxKleinStoryboard:
        """
        生成9宫格分镜

        Args:
            topic: 视频主题
            visual_anchor: Visual Anchor描述
                {
                    "name": "抱着木吉他的长发女孩",
                    "description": "穿着白色连衣裙，长发及腰，眼神温柔",
                    "key_feature": "手指拨动琴弦的动作"
                }
            tone_type: 调性类型 (静谧/情感, 悬疑/探索, 激烈/战斗)
            format: 视频比例 (9:16, 16:9)
        """
        tone = ToneType(tone_type) if tone_type in [e.value for e in ToneType] else ToneType.TRANQUIL
        adaptation = self.TONE_ADAPTATION[tone]

        # 生成9个镜头
        shots = self._generate_shots(topic, visual_anchor, adaptation, format)

        return FluxKleinStoryboard(
            board_id=self.board_id,
            topic=topic,
            visual_anchor=visual_anchor,
            tone_type=tone.value,
            shots=shots,
            format=format
        )

    def _generate_shots(
        self,
        topic: str,
        anchor: Dict,
        adaptation: Dict,
        format: str
    ) -> List[Dict]:
        """生成9个连贯镜头"""
        shots = []
        anchor_name = anchor.get("name", "主体")
        anchor_desc = anchor.get("description", "")
        anchor_feature = anchor.get("key_feature", "")

        for i, stage_config in enumerate(self.FLUID_STRUCTURE, 1):
            shot = {
                "shot_num": i,
                "stage": stage_config["objective"],
                "shot_type": stage_config["shot_type"],
                "camera_move": stage_config["camera_move"],
                "duration": stage_config["duration"],
                "format": format
            }

            # 根据阶段生成描述
            if i == 1:
                # 全景入画
                description = f"{topic}场景，{anchor_name}处于广阔环境中，"
                if tone := adaptation:
                    description += f"环境呈现{tone['connector']}效果，"
                description += f"画面建立整体氛围"
            elif i == 2:
                # 推进/聚焦
                description = f"镜头缓缓推进，聚焦{anchor_name}的{anchor_feature}细节，"
                description += "环境逐渐虚化，主体更加突出"
            elif i == 3:
                # 触发/诱因
                connector = adaptation["connector"]
                visual_cue = adaptation["visual_cue"]
                description = f"环境发生{connector}变化，{visual_cue}，"
                description += f"引起{anchor_name}的注意"
            elif i == 4:
                # 反应/互动
                motion = adaptation["motion"]
                description = f"{anchor_name}做出{motion}反应，"
                description += f"开始与场景互动"
            elif i == 5:
                # 过程/流动
                description = f"{anchor_name}正在进行动作，"
                description += f"镜头{self._get_camera_move_desc(stage_config['camera_move'])}，"
                description += "展现动作的连贯性"
            elif i == 6:
                # 高点/特写
                description = f"情绪达到高潮，聚焦{anchor_name}的{anchor_feature}瞬间，"
                description += f"捕捉关键表情或动作"
            elif i == 7:
                # 变化/后果
                description = f"由于动作，环境产生反馈，"
                description += f"画面展示变化效果"
            elif i == 8:
                # 余韵/局部
                description = f"镜头聚焦变化后的细节，"
                description += "捕捉微妙的光影效果"
            elif i == 9:
                # 拉远/出画
                description = f"镜头拉远，{anchor_name}与环境融为一体，"
                description += "画面逐渐拉远，形成完整叙事闭环"

            shot["description"] = description
            shot["prompt_en"] = self._build_prompt(shot, anchor, format)
            shot["tone"] = adaptation.get("connector", "平静")

            shots.append(shot)

        return shots

    def _get_camera_move_desc(self, move: str) -> str:
        """获取运镜描述"""
        move_descs = {
            "PUSH": "缓慢推进",
            "PULL": "平稳拉远",
            "PAN": "左右横移",
            "TILT": "上下升降",
            "ORBIT": "环绕旋转",
            "STATIC": "保持静止"
        }
        return move_descs.get(move, "缓慢移动")

    def _build_prompt(self, shot: Dict, anchor: Dict, format: str) -> str:
        """构建英文提示词 (用于FLUX-Klein)"""
        shot_type = shot["shot_type"]
        camera = shot["camera_move"]
        desc = shot["description"]

        # 转换景别
        shot_map = {
            "ELS": "extreme long shot",
            "LS": "long shot",
            "MS": "medium shot",
            "CU": "close-up",
            "ECU": "extreme close-up"
        }

        # 转换运镜
        camera_map = {
            "PUSH": "camera pushing forward",
            "PULL": "camera pulling back",
            "PAN": "camera panning",
            "TILT": "camera tilting",
            "ORBIT": "camera orbiting",
            "STATIC": "static shot"
        }

        prompt = f"{shot_map.get(shot_type, 'medium shot')}, {camera_map.get(camera, 'static')}, "
        prompt += f"{anchor.get('name', 'subject')}, {desc[:100]}, "
        prompt += f"cinematic lighting, high quality, 8k, "
        prompt += f"aspect ratio 9:16" if format == "9:16" else "aspect ratio 16:9"

        return prompt

    def export_for_flux_klein(self, board: FluxKleinStoryboard, output_dir: str) -> Dict:
        """导出为FLUX-Klein格式"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        results = {}

        # 1. 生成9行Prompt文件
        prompts_file = output_path / "flux_klein_prompts.txt"
        with open(prompts_file, "w", encoding="utf-8") as f:
            for i, shot in enumerate(board.shots, 1):
                f.write(f"Next Scene：{i}) {shot['shot_type']}/{shot['camera_move']} :: ")
                f.write(f"{shot['description']} :: {shot['tone']}\n")
            results["prompts"] = str(prompts_file)

        # 2. 生成JSON配置
        json_file = output_path / "flux_klein_board.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(board.to_dict(), f, ensure_ascii=False, indent=2)
        results["board"] = str(json_file)

        # 3. 生成ComfyUI格式
        comfyui_prompts = []
        for shot in board.shots:
            comfyui_prompts.append({
                "shot_num": shot["shot_num"],
                "prompt": shot["prompt_en"],
                "width": 1080 if board.format == "9:16" else 1920,
                "height": 1920 if board.format == "9:16" else 1080,
                "steps": 4,
                "cfg": 1,
                "seed": shot["shot_num"] * 1000000
            })

        comfyui_file = output_path / "flux_klein_comfyui.json"
        with open(comfyui_file, "w", encoding="utf-8") as f:
            json.dump(comfyui_prompts, f, ensure_ascii=False, indent=2)
        results["comfyui"] = str(comfyui_file)

        # 4. 生成SRT字幕
        srt_file = output_path / "flux_klein_subtitles.srt"
        with open(srt_file, "w", encoding="utf-8") as f:
            total_time = 0
            for i, shot in enumerate(board.shots, 1):
                start_ms = int(total_time * 1000)
                duration = shot["duration"]
                end_ms = int((total_time + duration) * 1000)

                start_time = self._ms_to_srt_time(start_ms)
                end_time = self._ms_to_srt_time(end_ms)

                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"[镜头{i}] {shot['description'][:50]}...\n\n")

                total_time += duration
            results["subtitles"] = str(srt_file)

        return results

    def _ms_to_srt_time(self, ms: int) -> str:
        """毫秒转SRT时间"""
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        milliseconds = ms % 1000
        return f"{minutes:02d}:{seconds:02d},{milliseconds:03d}"


# ============ 便捷函数 ============

def gen_flux_klein_board(
    topic: str,
    anchor_name: str,
    anchor_desc: str = "",
    anchor_feature: str = "",
    tone_type: str = "静谧/情感",
    format: str = "9:16"
) -> Dict:
    """
    生成FLUX-Klein 9宫格分镜

    Args:
        topic: 视频主题
        anchor_name: Visual Anchor名称
        anchor_desc: Visual Anchor描述
        anchor_feature: Visual Anchor关键特征
        tone_type: 调性类型
        format: 视频比例

    Returns:
        分镜JSON字典
    """
    generator = FluxKleinStoryboardGenerator()

    visual_anchor = {
        "name": anchor_name,
        "description": anchor_desc,
        "key_feature": anchor_feature
    }

    board = generator.generate(
        topic=topic,
        visual_anchor=visual_anchor,
        tone_type=tone_type,
        format=format
    )

    return board.to_dict()


# ============ CLI 入口 ============

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="FLUX-Klein 9宫格分镜生成器")
    parser.add_argument("--topic", "-t", required=True, help="视频主题")
    parser.add_argument("--anchor", "-a", required=True, help="Visual Anchor描述")
    parser.add_argument("--feature", "-f", default="", help="关键特征")
    parser.add_argument("--tone", "-T", default="静谧/情感",
                       choices=["静谧/情感", "悬疑/探索", "激烈/战斗"],
                       help="调性类型")
    parser.add_argument("--format", "-F", default="9:16",
                       choices=["9:16", "16:9"],
                       help="视频比例")
    parser.add_argument("--output", "-o", default="./outputs/flux_klein",
                       help="输出目录")

    args = parser.parse_args()

    # 生成分镜
    generator = FluxKleinStoryboardGenerator()
    board = generator.generate(
        topic=args.topic,
        visual_anchor={
            "name": args.anchor,
            "description": "",
            "key_feature": args.feature
        },
        tone_type=args.tone,
        format=args.format
    )

    # 导出
    results = generator.export_for_flux_klein(board, args.output)

    print("\n" + "=" * 60)
    print("FLUX-Klein 9宫格分镜生成完成！")
    print("=" * 60)
    print(f"主题: {args.topic}")
    print(f"调性: {args.tone}")
    print(f"比例: {args.format}")
    print(f"镜头数: {len(board.shots)}")
    print("=" * 60)
    print("\n生成文件:")
    for key, path in results.items():
        print(f"  {key}: {path}")

    # 打印9镜头预览
    print("\n" + "=" * 60)
    print("9镜头预览 (FLUX-Klein格式):")
    print("=" * 60)
    for i, shot in enumerate(board.shots, 1):
        print(f"Next Scene：{i}) {shot['shot_type']}/{shot['camera_move']} :: "
              f"{shot['description'][:40]}... :: {shot['tone']}")
