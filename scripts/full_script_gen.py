#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整剧本生成器
将FLUX-Klein分镜转换为完整视频剧本

包含:
- 分镜描述
- 旁白文案
- 音效设计
- BGM配乐
- 技术参数

作者: Claude Code
日期: 2026-02-07
"""

import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field
from pathlib import Path
from datetime import datetime


@dataclass
class SceneScript:
    """单场剧本"""
    scene_id: str
    shot_num: int
    duration: float
    # 画面
    visual_description: str
    shot_type: str
    camera_movement: str
    # 文案
    hook_line: str
    narration: str
    # 声音
    sfx: str
    bgm_style: str
    # 技术
    transition: str
    notes: str = ""


@dataclass
class FullScript:
    """完整剧本"""
    script_id: str
    topic: str
    format: str
    total_duration: float
    scenes: List[SceneScript]
    cta: str
    created_at: str = ""

    def to_dict(self) -> Dict:
        return {
            "script_id": self.script_id,
            "topic": self.topic,
            "format": self.format,
            "total_duration": self.total_duration,
            "scene_count": len(self.scenes),
            "scenes": [asdict(s) for s in self.scenes],
            "cta": self.cta,
            "created_at": self.created_at or datetime.now().isoformat()
        }


class FullScriptGenerator:
    """
    完整剧本生成器

    整合:
    - FLUX-Klein分镜数据
    - 奥斯卡级别五维结构
    - 声音设计
    """

    # BGM风格库
    BGM_STYLES = {
        "悬疑/探索": ["ambient_drone", "piano_tension", "string_stabs", "electronic_pulse"],
        "静谧/情感": ["soft_piano", "ambient_pad", "acoustic_guitar", "strings_swell"],
        "激烈/战斗": ["drum_kick", "synth_lead", "orchestra_hit", "distorted bass"],
        "科技": ["digital_beeps", "sci_fi_pad", "computer_hum", "futuristic_synth"]
    }

    # SFX音效库
    SFX_LIBRARY = {
        "悬疑/探索": ["keyboard_typing", "mouse_click", "screen_focus", "door_squeak", "footsteps"],
        "静谧/情感": ["wind_breeze", "nature_ambience", "soft_breath", "gentle_laugh"],
        "激烈/战斗": ["explosion", "gun_shot", "glass_break", "fast_movement"],
        "科技": ["ui_click", "system_boop", "loading_sound", "data_stream"]
    }

    def __init__(self):
        self.script_id = f"full_{int(time.time())}"

    def generate(
        self,
        topic: str,
        flux_board: Dict,
        tone_type: str = "悬疑/探索",
        cta: str = "评论区扣1领取资料"
    ) -> FullScript:
        """
        生成完整剧本

        Args:
            topic: 视频主题
            flux_board: FLUX-Klein分镜数据
            tone_type: 调性类型
            cta: 行动号召
        """
        shots = flux_board.get("shots", [])
        video_format = flux_board.get("format", "16:9")

        scenes = []
        total_duration = 0

        for i, shot in enumerate(shots, 1):
            scene = self._build_scene(i, shot, tone_type, video_format)
            scenes.append(scene)
            total_duration += scene.duration

        return FullScript(
            script_id=self.script_id,
            topic=topic,
            format=video_format,
            total_duration=total_duration,
            scenes=scenes,
            cta=cta
        )

    def _build_scene(
        self,
        num: int,
        shot: Dict,
        tone_type: str,
        video_format: str
    ) -> SceneScript:
        """构建单场"""
        stage = shot.get("stage", "")
        desc = shot.get("description", "")
        shot_type = shot.get("shot_type", "MS")
        camera = shot.get("camera_move", "STATIC")

        # 根据镜头阶段生成文案
        if num == 1:
            hook = "别再用传统方式了！"
            narration = self._gen_opening_narration(desc)
        elif num == 2:
            hook = "看这个变化"
            narration = self._gen_reveal_narration(desc)
        elif num == 3:
            hook = "注意到了吗？"
            narration = self._gen_building_narration(desc)
        elif num == 4:
            hook = "反应来了"
            narration = self._gen_reaction_narration(desc)
        elif num == 5:
            hook = "高潮迭起"
            narration = self._gen_climax_narration(desc)
        elif num == 6:
            hook = "就是这个瞬间"
            narration = self._gen_peak_narration(desc)
        elif num == 7:
            hook = "看仔细了"
            narration = self._gen_reveal_narration(desc)
        elif num == 8:
            hook = "细节在这里"
            narration = self._gen_detail_narration(desc)
        else:
            hook = "未来已来"
            narration = self._gen_closing_narration(desc)

        return SceneScript(
            scene_id=f"{num:02d}",
            shot_num=num,
            duration=shot.get("duration", 8.0),
            visual_description=desc,
            shot_type=shot_type,
            camera_movement=camera,
            hook_line=hook,
            narration=narration,
            sfx=self._get_sfx(num, tone_type),
            bgm_style=self._get_bgm(num, tone_type),
            transition=self._get_transition(num),
            notes=self._get_camera_notes(shot_type, camera)
        )

    def _gen_opening_narration(self, desc: str) -> str:
        """开场旁白"""
        return "还在用传统方式做XX？效率低还费时。"

    def _gen_reveal_narration(self, desc: str) -> str:
        """揭示旁白"""
        return "直到DeepSeek出现，一切都变了。"

    def _gen_building_narration(self, desc: str) -> str:
        """铺垫旁白"""
        return "看清楚了，这里有个关键变化。"

    def _gen_reaction_narration(self, desc: str) -> str:
        """反应旁白"""
        return "这就是反应，表情说明了一切。"

    def _gen_climax_narration(self, desc: str) -> str:
        """高潮旁白"""
        return "高潮来了，这才是真正的实力。"

    def _gen_peak_narration(self, desc: str) -> str:
        """巅峰旁白"""
        return "这个瞬间，价值千金。"

    def _gen_detail_narration(self, desc: str) -> str:
        """细节旁白"""
        return "细节决定成败，看这里。"

    def _gen_closing_narration(self, desc: str) -> str:
        """收尾旁白"""
        return "未来已经来了，就在你眼前。"

    def _get_sfx(self, num: int, tone_type: str) -> str:
        """获取音效"""
        sfx_list = self.SFX_LIBRARY.get(tone_type, self.SFX_LIBRARY["科技"])
        if num == 1:
            return sfx_list[0] if len(sfx_list) > 0 else "keyboard_typing"
        elif num <= 3:
            return sfx_list[1] if len(sfx_list) > 1 else "mouse_click"
        elif num <= 6:
            return sfx_list[2] if len(sfx_list) > 2 else "screen_focus"
        else:
            return sfx_list[3] if len(sfx_list) > 3 else "ambient_noise"

    def _get_bgm(self, num: int, tone_type: str) -> str:
        """获取BGM"""
        bgm_list = self.BGM_STYLES.get(tone_type, self.BGM_STYLES["科技"])
        if num == 1:
            return "tension_build"
        elif num <= 4:
            return bgm_list[0] if bgm_list else "ambient"
        elif num <= 6:
            return bgm_list[1] if len(bgm_list) > 1 else "piano"
        elif num <= 8:
            return bgm_list[2] if len(bgm_list) > 2 else "strings"
        else:
            return "resolution"

    def _get_transition(self, num: int) -> str:
        """获取转场"""
        if num == 1:
            return "fade_in"
        elif num == 3:
            return "dissolve"
        elif num == 6:
            return "match_cut"
        elif num == 9:
            return "fade_out"
        else:
            return "cut"

    def _get_camera_notes(self, shot_type: str, camera: str) -> str:
        """获取摄影笔记"""
        notes = {
            "ELS": "大远景，建立镜头",
            "LS": "远景，展示环境",
            "MS": "中景，标准叙事",
            "CU": "特写，强调细节",
            "ECU": "大特写，情绪高点"
        }
        camera_notes = {
            "PUSH": "推进",
            "PULL": "拉远",
            "PAN": "横移",
            "ORBIT": "环绕",
            "STATIC": "固定"
        }
        return f"{notes.get(shot_type, '')} + {camera_notes.get(camera, '')}"

    def export(self, script: FullScript, output_dir: str) -> Dict:
        """导出剧本"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        results = {}

        # 1. 完整JSON
        json_file = output_path / "full_script.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(script.to_dict(), f, ensure_ascii=False, indent=2)
        results["script"] = str(json_file)

        # 2. 简明表格
        table_file = output_path / "script_table.md"
        with open(table_file, "w", encoding="utf-8") as f:
            f.write(f"# {script.topic} - 完整剧本\n\n")
            f.write(f"**格式**: {script.format} | **时长**: {script.total_duration}秒 | **场景数**: {len(script.scenes)}\n\n")
            f.write("| 场景 | 镜头 | 时长 | 画面 | 旁白 | 音效 | BGM | 转场 |\n")
            f.write("|------|------|------|------|------|------|------|------|\n")
            for scene in script.scenes:
                f.write(f"| {scene.scene_id} | {scene.shot_type} | {scene.duration}s | {scene.visual_description[:30]}... | {scene.narration[:20]}... | {scene.sfx} | {scene.bgm_style} | {scene.transition} |\n")
        results["table"] = str(table_file)

        # 3. 分镜表
        storyboard_file = output_path / "storyboard.md"
        with open(storyboard_file, "w", encoding="utf-8") as f:
            f.write(f"# {script.topic} - 分镜表\n\n")
            for scene in script.scenes:
                f.write(f"## 场景 {scene.scene_id} (镜头{scene.shot_num})\n\n")
                f.write(f"**时长**: {scene.duration}秒 | **镜头**: {scene.shot_type} | **运镜**: {scene.camera_movement}\n\n")
                f.write(f"**画面**: {scene.visual_description}\n\n")
                f.write(f"**钩子**: {scene.hook_line}\n\n")
                f.write(f"**旁白**: {scene.narration}\n\n")
                f.write(f"**音效**: {scene.sfx} | **配乐**: {scene.bgm_style} | **转场**: {scene.transition}\n\n")
                f.write(f"**备注**: {scene.notes}\n\n")
                f.write("---\n\n")
        results["storyboard"] = str(storyboard_file)

        # 4. 旁白稿
        voice_file = output_path / "voiceover.txt"
        with open(voice_file, "w", encoding="utf-8") as f:
            total_time = 0
            for scene in script.scenes:
                start = int(total_time)
                end = int(total_time + scene.duration)
                f.write(f"[{start:02d}:{start%60:02d}-{end:02d}:{end%60:02d}] {scene.narration}\n")
                total_time += scene.duration
        results["voiceover"] = str(voice_file)

        # 5. 技术表
        tech_file = output_path / "tech_specs.md"
        with open(tech_file, "w", encoding="utf-8") as f:
            f.write(f"# {script.topic} - 技术规格\n\n")
            f.write("## 基础信息\n\n")
            f.write(f"- **格式**: {script.format}\n")
            f.write(f"- **总时长**: {script.total_duration}秒\n")
            f.write(f"- **帧率**: 30fps\n")
            f.write(f"- **场景数**: {len(script.scenes)}\n\n")
            f.write("## 分镜详情\n\n")
            f.write("| 场景 | 类型 | 运镜 | 时长 | 转场 |\n")
            f.write("|------|------|------|------|------|\n")
            for scene in script.scenes:
                f.write(f"| {scene.scene_id} | {scene.shot_type} | {scene.camera_movement} | {scene.duration}s | {scene.transition} |\n")
        results["tech_specs"] = str(tech_file)

        return results


# ============ CLI ============

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="完整剧本生成器")
    parser.add_argument("--topic", "-t", required=True, help="视频主题")
    parser.add_argument("--board", "-b", required=True, help="FLUX-Klein分镜JSON文件")
    parser.add_argument("--tone", "-T", default="悬疑/探索", help="调性类型")
    parser.add_argument("--cta", "-c", default="评论区扣1领取资料", help="行动号召")
    parser.add_argument("--output", "-o", default="./outputs/full_script", help="输出目录")

    args = parser.parse_args()

    # 读取分镜
    with open(args.board, "r", encoding="utf-8") as f:
        board = json.load(f)

    # 生成剧本
    generator = FullScriptGenerator()
    script = generator.generate(args.topic, board, args.tone, args.cta)

    # 导出
    results = generator.export(script, args.output)

    print("\n" + "=" * 60)
    print("完整剧本生成完成！")
    print("=" * 60)
    print(f"主题: {args.topic}")
    print(f"格式: {script.format}")
    print(f"时长: {script.total_duration}秒")
    print(f"场景: {len(script.scenes)}个")
    print("=" * 60)
    print("\n生成文件:")
    for key, path in results.items():
        print(f"  {key}: {path}")
