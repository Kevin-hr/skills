#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
奥斯卡级别视频脚本生成器
基于 viral-creative-lead + sora-film-director 标准
5维脚本结构：Style(风格) + Prose(文案) + Cinematography(摄影) + Actions(动作) + Sound(声音)

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


class VideoFormat(Enum):
    """视频规格"""
    VERTICAL = "9:16"      # 抖音/小红书
    HORIZONTAL = "16:9"   # B站/YouTube
    SQUARE = "1:1"        # Instagram


class ShotScale(Enum):
    """镜头尺度 - 电影级标准"""
    ELS = "ELS"  # Extreme Long Shot - 建立镜头
    LS = "LS"   # Long Shot - 全身
    MS = "MS"   # Medium Shot - 中景
    CU = "CU"   # Close-Up - 特写
    ECU = "ECU" # Extreme Close-Up - 大特写


class CameraMovement(Enum):
    """运镜方式"""
    STATIC = "static"              # 静态
    PUSH_FORWARD = "push_forward"  # 推进
    PULL_BACK = "pull_back"        # 拉远
    PAN_LEFT = "pan_left"          # 左摇
    PAN_RIGHT = "pan_right"        # 右摇
    TILT_UP = "tilt_up"            # 上摇
    TILT_DOWN = "tilt_down"        # 下摇
    DOLLY_TRACK = "dolly_track"    # 滑轨
    ZOOM_IN = "zoom_in"            # 变焦推进
    ZOOM_OUT = "zoom_out"          # 变焦拉远


class MotionState(Enum):
    """运动状态"""
    STATIC = "static"              # 静态主体
    SUBTLE = "subtle"              # 微动
    MODERATE = "moderate"           # 中等运动
    DYNAMIC = "dynamic"            # 动态
    EXTREME = "extreme"           # 极致运动


class VisualStyle(Enum):
    """视觉风格"""
    CYBERPUNK = "cyberpunk"           # 赛博朋克
    MINIMAL = "minimal"               # 极简主义
    CINEMATIC = "cinematic"           # 电影质感
    RETRO = "retro"                  # 复古
    FUTURISTIC = "futuristic"         # 未来感
    NATURAL = "natural"              # 自然真实


@dataclass
class FiveDimension:
    """五维脚本结构"""
    # Style (风格)
    visual_style: str = "cinematic"
    color_grading: str = "电影感调色"
    lighting: str = "三点布光"
    vibe: str = "专业"

    # Prose (文案)
    hook_line: str = ""
    body_lines: List[str] = field(default_factory=list)
    cta_line: str = ""

    # Cinematography (摄影)
    shot_scale: str = "MS"  # 默认中景
    camera_movement: str = "static"
    aspect_ratio: str = "9:16"

    # Actions (动作)
    motion_state: str = "subtle"
    motion_descriptor: str = "微风吹过"
    transition: str = "cut"

    # Sound (声音)
    narrative: str = ""
    sfx: str = ""
    bgm_style: str = "科技感"


@dataclass
class SceneData:
    """单个场景数据"""
    scene_id: str
    duration: float  # 秒
    order: int
    five_dimension: FiveDimension

    def to_dict(self) -> Dict:
        return {
            "scene_id": self.scene_id,
            "duration": self.duration,
            "order": self.order,
            "five_dimension": asdict(self.five_dimension)
        }


@dataclass
class OscarScript:
    """奥斯卡级别完整脚本"""
    script_id: str
    topic: str
    format: str
    total_duration: float
    scenes: List[SceneData]
    distribution: Dict = field(default_factory=dict)
    created_at: str = ""

    def to_dict(self) -> Dict:
        return {
            "script_id": self.script_id,
            "topic": self.topic,
            "format": self.format,
            "total_duration": self.total_duration,
            "scene_count": len(self.scenes),
            "scenes": [s.to_dict() for s in self.scenes],
            "distribution": self.distribution,
            "created_at": self.created_at or datetime.now().isoformat()
        }


class OscarScriptGenerator:
    """
    奥斯卡级别脚本生成器

    基于 viral-creative-lead 创意策略：
    - 第一性原理 (First Principle)
    - 剧情反转 (Twist)
    - 情绪弧线 (Emotional Arc)

    基于 sora-film-director 导演规范：
    - 5维脚本结构
    - 镜头语言
    - 运镜设计
    """

    # 情绪弧线模板
    EMOTIONAL_ARCS = {
        "problem_solution": {
            "name": "问题-解决方案",
            "arc": ["frustration", "curiosity", "realization", "excitement", "action"],
            "description": "先制造痛点，再给出解决方案"
        },
        "contrast_reveal": {
            "name": "对比揭示",
            "arc": ["confusion", "surprise", "comparison", "clarity", "conviction"],
            "description": "通过对比揭示真相"
        },
        "journey": {
            "name": "成长旅程",
            "arc": ["challenge", "struggle", "breakthrough", "success", "invitation"],
            "description": "跟随主角成长，引发共鸣"
        },
        "mystery": {
            "name": "悬念揭秘",
            "arc": ["intrigue", "suspense", "tension", "reveal", "resolution"],
            "description": "层层递进，最后揭秘"
        }
    }

    # 视觉风格参数库
    STYLE_PRESETS = {
        "cyberpunk": {
            "colors": ["#00D4FF", "#7B2FFF", "#FF6B35"],
            "lighting": "霓虹光效 + 暗部补光",
            "vibe": "赛博朋克",
            "text_effect": "故障风 + 发光"
        },
        "cinematic": {
            "colors": ["#1A1A2E", "#16213E", "#0F3460"],
            "lighting": "高对比度 + 柔和过渡",
            "vibe": "电影质感",
            "text_effect": "渐显 + 阴影"
        },
        "minimal": {
            "colors": ["#FFFFFF", "#F5F5F5", "#333333"],
            "lighting": "自然光 + 简单补光",
            "vibe": "极简专业",
            "text_effect": "简洁无衬线"
        },
        "futuristic": {
            "colors": ["#00FF87", "#60EFFF", "#FFFFFF"],
            "lighting": "全息光效",
            "vibe": "未来科技",
            "text_effect": "全息投影 + 粒子"
        }
    }

    # 平台规格
    PLATFORM_SPECS = {
        "9:16": {"width": 1080, "height": 1920, "platforms": ["抖音", "小红书", "视频号"]},
        "16:9": {"width": 1920, "height": 1080, "platforms": ["B站", "YouTube", "微信"]},
        "1:1":  {"width": 1080, "height": 1080, "platforms": ["Instagram", "微博"]}
    }

    def __init__(self):
        self.script_id = f"oscar_{int(time.time())}"

    def generate(
        self,
        topic: str,
        emotional_arc: str = "problem_solution",
        visual_style: str = "cinematic",
        video_format: VideoFormat = VideoFormat.VERTICAL,
        platform: str = "抖音"
    ) -> OscarScript:
        """
        生成奥斯卡级别脚本

        Args:
            topic: 视频主题
            emotional_arc: 情绪弧线类型
            visual_style: 视觉风格
            video_format: 视频规格
            platform: 目标平台
        """
        arc_config = self.EMOTIONAL_ARCS.get(emotional_arc, self.EMOTIONAL_ARCS["problem_solution"])
        style_config = self.STYLE_PRESETS.get(visual_style, self.STYLE_PRESETS["cinematic"])

        # 根据主题生成场景
        scenes = self._build_scenes(topic, arc_config, style_config, video_format)

        # 生成分发策略
        distribution = self._gen_distribution(topic, visual_style, platform)

        return OscarScript(
            script_id=self.script_id,
            topic=topic,
            format=video_format.value,
            total_duration=sum(s.duration for s in scenes),
            scenes=scenes,
            distribution=distribution
        )

    def _build_scenes(
        self,
        topic: str,
        arc_config: Dict,
        style_config: Dict,
        video_format: VideoFormat
    ) -> List[SceneData]:
        """构建场景序列"""

        aspect_ratio = video_format.value

        if topic.lower() in ["deepseek", "ds"]:
            return self._gen_deepseek_scenes(arc_config, style_config, aspect_ratio)
        elif "ai" in topic.lower() or "工具" in topic:
            return self._gen_tool_review_scenes(topic, arc_config, style_config, aspect_ratio)
        else:
            return self._gen_generic_scenes(topic, arc_config, style_config, aspect_ratio)

    def _gen_deepseek_scenes(self, arc_config, style_config, aspect_ratio) -> List[SceneData]:
        """DeepSeek专题场景 - 奥斯卡级别"""

        scenes = []

        # 场景1: 建立镜头 - 制造悬念
        scenes.append(SceneData(
            scene_id="01",
            duration=3.0,
            order=1,
            five_dimension=FiveDimension(
                visual_style=style_config["vibe"],
                color_grading="冷色调 + 高对比",
                lighting="低光环境 + 聚光灯",
                vibe="神秘感",
                hook_line="别再用传统方式了！这个DeepSeek免费还更强",
                body_lines=[
                    "还在为效率发愁？",
                    "还在为成本烦恼？",
                    "AI时代的选择题，答案已经变了"
                ],
                cta_line="往下看，颠覆你的认知",
                shot_scale=ShotScale.ELS.value,
                camera_movement=CameraMovement.PUSH_FORWARD.value,
                aspect_ratio=aspect_ratio,
                motion_state=MotionState.STATIC.value,
                motion_descriptor="镜头缓慢推进",
                transition="dissolve",
                narrative="别再用传统方式了...",
                sfx="心跳声 + 倒计时",
                bgm_style="悬疑紧张"
            )
        ))

        # 场景2: 痛点场景 - 情绪低谷
        scenes.append(SceneData(
            scene_id="02",
            duration=8.0,
            order=2,
            five_dimension=FiveDimension(
                visual_style="realistic",
                color_grading="灰暗 + 低饱和",
                lighting="自然光偏暗",
                vibe="沮丧",
                hook_line="曾经的我们",
                body_lines=[
                    "熬夜加班到凌晨",
                    "效率却始终上不去",
                    "工具一堆，真正管用的没几个"
                ],
                cta_line="说的是不是你？",
                shot_scale=ShotScale.LS.value,
                camera_movement=CameraMovement.STATIC.value,
                aspect_ratio=aspect_ratio,
                motion_state=MotionState.SUBTLE.value,
                motion_descriptor="轻微手持晃动",
                transition="cut",
                narrative="曾经的我...",
                sfx="键盘声 + 叹息声",
                bgm_style="低沉钢琴"
            )
        ))

        # 场景3: 转折点 - 揭示解决方案
        scenes.append(SceneData(
            scene_id="03",
            duration=15.0,
            order=3,
            five_dimension=FiveDimension(
                visual_style=style_config["vibe"],
                color_grading="渐变：从冷到暖",
                lighting="三点布光 + 主光强调",
                vibe="兴奋",
                hook_line="直到我遇见了它",
                body_lines=[
                    "DeepSeek - 国产AI之光",
                    "免费 + 开源 + 强大",
                    "三步搞定复杂任务"
                ],
                cta_line="来看看它的表现",
                shot_scale=ShotScale.MS.value,
                camera_movement=CameraMovement.DOLLY_TRACK.value,
                aspect_ratio=aspect_ratio,
                motion_state=MotionState.MODERATE.value,
                motion_descriptor="平滑横移",
                transition="wipe_left",
                narrative="直到那一天...",
                sfx="科技感转场音效",
                bgm_style="电子激励"
            )
        ))

        # 场景4: 核心展示 - 功能演示
        scenes.append(SceneData(
            scene_id="04",
            duration=25.0,
            order=4,
            five_dimension=FiveDimension(
                visual_style="screen_recording",
                color_grading="原色还原",
                lighting="屏幕发光",
                vibe="专业",
                hook_line="实操演示",
                body_lines=[
                    "第一步：输入需求",
                    "第二步：AI理解意图",
                    "第三步：高质量输出"
                ],
                cta_line="就这么简单",
                shot_scale=ShotScale.CU.value,
                camera_movement=CameraMovement.ZOOM_IN.value,
                aspect_ratio=aspect_ratio,
                motion_state=MotionState.DYNAMIC.value,
                motion_descriptor="界面动画流畅",
                transition="cross_dissolve",
                narrative="看好了...",
                sfx="鼠标点击 + 生成音效",
                bgm_style="轻快电子"
            )
        ))

        # 场景5: 效果对比 - 视觉冲击
        scenes.append(SceneData(
            scene_id="05",
            duration=15.0,
            order=5,
            five_dimension=FiveDimension(
                visual_style="split_comparison",
                color_grading="左右对比色",
                lighting="双区域独立",
                vibe="震撼",
                hook_line="差距，一目了然",
                body_lines=[
                    "左边：传统方式（耗时1小时）",
                    "右边：DeepSeek（3分钟）",
                    "效率提升20倍不止"
                ],
                cta_line="这就是AI的力量",
                shot_scale=ShotScale.ECU.value,
                camera_movement=CameraMovement.STATIC.value,
                aspect_ratio=aspect_ratio,
                motion_state=MotionState.SUBTLE.value,
                motion_descriptor="对比动画",
                transition="match_cut",
                narrative="对比一下...",
                sfx="对比音效 + 惊叹声",
                bgm_style="渐进高潮"
            )
        ))

        # 场景6: 总结升华 - 行动号召
        scenes.append(SceneData(
            scene_id="06",
            duration=8.0,
            order=6,
            five_dimension=FiveDimension(
                visual_style=style_config["vibe"],
                color_grading="暖色调收尾",
                lighting="柔和环绕光",
                vibe="温暖希望",
                hook_line="未来已经来了",
                body_lines=[
                    "拥抱AI，拥抱变化",
                    "DeepSeek，你的AI伙伴",
                    "免费使用，门槛超低"
                ],
                cta_line="评论区扣【1】，领取使用指南",
                shot_scale=ShotScale.MS.value,
                camera_movement=CameraMovement.PULL_BACK.value,
                aspect_ratio=aspect_ratio,
                motion_state=MotionState.SUBTLE.value,
                motion_descriptor="镜头缓慢拉远",
                transition="fade_out",
                narrative="未来已经来了...",
                sfx="希望感音效",
                bgm_style="温暖弦乐"
            )
        ))

        return scenes

    def _gen_tool_review_scenes(self, topic, arc_config, style_config, aspect_ratio) -> List[SceneData]:
        """通用工具评测场景"""
        scenes = []

        # 简化版5场景结构
        scenes.append(SceneData(
            scene_id="01", duration=3.0, order=1,
            five_dimension=FiveDimension(
                visual_style=style_config["vibe"],
                hook_line=f"别再用传统方式了！这个{topic}免费还更强",
                shot_scale=ShotScale.ELS.value,
                camera_movement=CameraMovement.PUSH_FORWARD.value,
                aspect_ratio=aspect_ratio
            )
        ))

        scenes.append(SceneData(
            scene_id="02", duration=10.0, order=2,
            five_dimension=FiveDimension(
                visual_style="realistic",
                hook_line="还在用老方法？",
                shot_scale=ShotScale.LS.value,
                camera_movement=CameraMovement.STATIC.value,
                aspect_ratio=aspect_ratio
            )
        ))

        scenes.append(SceneData(
            scene_id="03", duration=30.0, order=3,
            five_dimension=FiveDimension(
                visual_style="demo",
                hook_line=f"{topic} 核心功能演示",
                shot_scale=ShotScale.CU.value,
                camera_movement=CameraMovement.DOLLY_TRACK.value,
                aspect_ratio=aspect_ratio,
                motion_state=MotionState.MODERATE.value
            )
        ))

        scenes.append(SceneData(
            scene_id="04", duration=20.0, order=4,
            five_dimension=FiveDimension(
                visual_style="comparison",
                hook_line="效果对比",
                shot_scale=ShotScale.MS.value,
                camera_movement=CameraMovement.ZOOM_IN.value,
                aspect_ratio=aspect_ratio
            )
        ))

        scenes.append(SceneData(
            scene_id="05", duration=10.0, order=5,
            five_dimension=FiveDimension(
                visual_style=style_config["vibe"],
                hook_line=f"推荐{topic}",
                shot_scale=ShotScale.MS.value,
                camera_movement=CameraMovement.PULL_BACK.value,
                aspect_ratio=aspect_ratio,
                cta_line="评论区扣1"
            )
        ))

        return scenes

    def _gen_generic_scenes(self, topic, arc_config, style_config, aspect_ratio) -> List[SceneData]:
        """通用场景"""
        return self._gen_tool_review_scenes(topic, arc_config, style_config, aspect_ratio)

    def _gen_distribution(self, topic: str, visual_style: str, platform: str) -> Dict:
        """生成分发策略"""
        return {
            "cover_prompt": f"{visual_style}风格, {topic}, 大字标题, 高清质感",
            "titles": [
                f"别再用传统方式了！这个{topic}免费还更强",
                f"{topic}大揭秘，99%的人都不知道",
                f"用了{topic}后，我的效率提升了10倍"
            ],
            "description": f"深度测评{topic}，AI工具如何改变生活",
            "hashtags": [f"#{topic}", "#AI工具", "#效率提升", "#科技"],
            "platforms": [platform],
            "best发布时间": "12:00-14:00 或 20:00-22:00"
        }

    def export_for_production(self, script: OscarScript, output_dir: str) -> Dict:
        """
        导出为生产文件 - 供 sora-film-director 使用

        生成:
        - 1_midjourney_prompts.txt
        - 2_voiceover_script.txt
        - 3_wan_config.json
        - 5_subtitles.srt
        - 6_distribution_kit.md
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        results = {}

        # 1. Midjourney Prompts
        prompts_file = output_path / "1_midjourney_prompts.txt"
        with open(prompts_file, "w", encoding="utf-8") as f:
            for scene in script.scenes:
                fd = scene.five_dimension
                prompt = self._build_midjourney_prompt(fd, script.format)
                f.write(f"Scene {scene.scene_id} ({scene.duration}s):\n")
                f.write(f"{prompt}\n\n")
            results["midjourney_prompts"] = str(prompts_file)

        # 2. Voiceover Script
        voiceover_file = output_path / "2_voiceover_script.txt"
        with open(voiceover_file, "w", encoding="utf-8") as f:
            total_duration = 0
            for scene in script.scenes:
                fd = scene.five_dimension
                start_time = total_duration
                end_time = total_duration + scene.duration
                f.write(f"[{start_time:05.1f}s - {end_time:05.1f}s] Scene {scene.scene_id}\n")
                f.write(f"Hook: {fd.hook_line}\n")
                f.write(f"Narration: {fd.narrative}\n")
                f.write(f"SFX: {fd.sfx}\n")
                f.write(f"BGM: {fd.bgm_style}\n")
                f.write("-" * 40 + "\n")
                total_duration = end_time
            results["voiceover_script"] = str(voiceover_file)

        # 3. Wan Config (i2v)
        wan_config = {
            "project_info": {
                "topic": script.topic,
                "format": script.format,
                "total_duration": script.total_duration
            },
            "scenes": []
        }
        for scene in script.scenes:
            fd = scene.five_dimension
            wan_config["scenes"].append({
                "scene_id": scene.scene_id,
                "duration": scene.duration,
                "i2v_wan": {
                    "prompt": f"{fd.visual_style}, {fd.hook_line}, {fd.motion_descriptor}",
                    "motion_descriptor": fd.motion_state,
                    "camera_movement": fd.camera_movement,
                    "speed_curve": f"0-{scene.duration}s: constant",
                    "zoom": "1.0x to 1.2x" if fd.camera_movement in ["push_forward", "zoom_in"] else "1.0x"
                }
            })

        wan_file = output_path / "3_wan_config.json"
        with open(wan_file, "w", encoding="utf-8") as f:
            json.dump(wan_config, f, ensure_ascii=False, indent=2)
        results["wan_config"] = str(wan_file)

        # 5. Subtitles (SRT)
        srt_file = output_path / "5_subtitles.srt"
        with open(srt_file, "w", encoding="utf-8") as f:
            total_duration_ms = 0
            for idx, scene in enumerate(script.scenes, 1):
                fd = scene.five_dimension
                start_ms = int(total_duration_ms * 1000)
                end_ms = int((total_duration_ms + scene.duration) * 1000)

                start_time = self._ms_to_srt_time(start_ms)
                end_time = self._ms_to_srt_time(end_ms)

                f.write(f"{idx}\n")
                f.write(f"{start_time} --> {end_time}\n")
                # 简化：每场景显示主要hook
                f.write(f"{fd.hook_line}\n\n")
                total_duration_ms += scene.duration
            results["subtitles"] = str(srt_file)

        # 6. Distribution Kit
        dist_file = output_path / "6_distribution_kit.md"
        with open(dist_file, "w", encoding="utf-8") as f:
            f.write(f"# {script.topic} - 分发套件\n\n")
            f.write(f"**格式**: {script.format} | **时长**: {script.total_duration}秒 | **场景数**: {len(script.scenes)}\n\n")
            f.write("## 封面提示词\n\n")
            f.write(f"{script.distribution.get('cover_prompt', '')}\n\n")
            f.write("## 标题选项\n\n")
            for title in script.distribution.get("titles", []):
                f.write(f"- {title}\n")
            f.write("\n## 话题标签\n\n")
            for tag in script.distribution.get("hashtags", []):
                f.write(f"{tag} ")
            f.write("\n\n## 最佳发布时间\n\n")
            f.write(f"{script.distribution.get('best发布时间', '待定')}\n")
            results["distribution_kit"] = str(dist_file)

        return results

    def _build_midjourney_prompt(self, fd: FiveDimension, aspect_ratio: str) -> str:
        """构建Midjourney提示词"""
        ratio_map = {"9:16": "--ar 9:16", "16:9": "--ar 16:9", "1:1": "--ar 1:1"}
        return f"{fd.visual_style}风格, {fd.hook_line}, {fd.color_grading}, {fd.lighting}, 电影质感, 高清8k, {ratio_map.get(aspect_ratio, '--ar 9:16')}"

    def _ms_to_srt_time(self, ms: int) -> str:
        """毫秒转SRT时间格式"""
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        hours = minutes // 60
        minutes = minutes % 60
        milliseconds = ms % 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


# ============ 便捷函数 ============

def gen_oscar_script(
    topic: str,
    emotional_arc: str = "problem_solution",
    visual_style: str = "cinematic",
    format: str = "9:16"
) -> Dict:
    """
    生成奥斯卡级别脚本

    Args:
        topic: 视频主题
        emotional_arc: 情绪弧线 (problem_solution/contrast_reveal/journey/mystery)
        visual_style: 视觉风格 (cyberpunk/cinematic/minimal/futuristic)
        format: 视频规格 (9:16/16:9/1:1)

    Returns:
        脚本字典
    """
    generator = OscarScriptGenerator()
    script = generator.generate(
        topic=topic,
        emotional_arc=emotional_arc,
        visual_style=visual_style,
        video_format=VideoFormat(format)
    )
    return script.to_dict()


def export_for_comfyui(script_dict: Dict, output_dir: str) -> Dict:
    """导出为ComfyUI可用格式"""
    generator = OscarScriptGenerator()
    # 临时创建script对象
    scenes = []
    for s in script_dict.get("scenes", []):
        fd = FiveDimension(**s["five_dimension"])
        scenes.append(SceneData(
            scene_id=s["scene_id"],
            duration=s["duration"],
            order=s["order"],
            five_dimension=fd
        ))

    class TempScript:
        def __init__(self):
            self.scenes = scenes
            self.topic = script_dict["topic"]
            self.format = script_dict["format"]
            self.distribution = script_dict.get("distribution", {})

    return generator.export_for_production(TempScript(), output_dir)


# ============ CLI 入口 ============

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="奥斯卡级别视频脚本生成器")
    parser.add_argument("--topic", "-t", required=True, help="视频主题")
    parser.add_argument("--arc", "-a", default="problem_solution",
                       choices=["problem_solution", "contrast_reveal", "journey", "mystery"],
                       help="情绪弧线类型")
    parser.add_argument("--style", "-s", default="cinematic",
                       choices=["cyberpunk", "cinematic", "minimal", "futuristic"],
                       help="视觉风格")
    parser.add_argument("--format", "-f", default="9:16",
                       choices=["9:16", "16:9", "1:1"],
                       help="视频规格")
    parser.add_argument("--output", "-o", default="./outputs/oscar_script",
                       help="输出目录")
    parser.add_argument("--platform", "-p", default="抖音", help="目标平台")

    args = parser.parse_args()

    # 生成脚本
    generator = OscarScriptGenerator()
    script = generator.generate(
        topic=args.topic,
        emotional_arc=args.arc,
        visual_style=args.style,
        video_format=VideoFormat(args.format),
        platform=args.platform
    )

    # 导出生产文件
    results = generator.export_for_production(script, args.output)

    print("\n" + "=" * 60)
    print("奥斯卡级别脚本生成完成！")
    print("=" * 60)
    print(f"主题: {script.topic}")
    print(f"格式: {script.format}")
    print(f"时长: {script.total_duration}秒")
    print(f"场景数: {len(script.scenes)}")
    print("=" * 60)
    print("\n生成文件:")
    for key, path in results.items():
        print(f"  {key}: {path}")

    # 保存脚本JSON
    script_file = Path(args.output) / "oscar_script.json"
    with open(script_file, "w", encoding="utf-8") as f:
        json.dump(script.to_dict(), f, ensure_ascii=False, indent=2)
    print(f"\n脚本文件: {script_file}")
