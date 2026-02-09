#!/usr/bin/env python3
"""
Auto File Organizer - 自动化文件整理工具

Usage:
    python auto_organize.py --target /path/to/folder
    python auto_organize.py --target /path --dry-run  # 预览模式
    python auto_organize.py --target /path --config custom_patterns.json
"""

import os
import re
import json
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class PatternRule:
    """文件分类规则"""
    name: str
    patterns: List[str]
    target_folder: str
    priority: int = 0


# 默认分类模式
DEFAULT_PATTERNS = [
    # WeChat 公众号配图
    PatternRule("WeChat", ["wx_*.png", "*2025*.jpg", "*2025*.webp", "*2026*.jpg",
                           "*2026*.webp", "*公众号*.jpg", "*拆穿*.jpg", "*电商流程*.jpg",
                           "*AI大分享*.webp"], "WeChat", priority=1),
    # 小红书
    PatternRule("XiaoHongShu", ["*小红书*.jpg", "*1083*.jpeg"], "XiaoHongShu", priority=2),
    # 封面/爆款图
    PatternRule("Covers", ["*爆款*.png", "*封面*.png", "*1.png", "OM5E3DBT.jpg",
                          "*1769527926084*.jpeg"], "Covers", priority=3),
    # AI 资源
    PatternRule("AI-Resources", ["*雲帆*.png", "*AI*.png", "*开发思想*.png",
                                 "fJ8*.jpeg", "*11acaebc*.jpeg", "1月29日.png"], "AI-Resources", priority=4),
    # 壁纸
    PatternRule("Wallpapers", ["*.jpg", "*.png", "*.webp"], "Wallpapers", priority=10),
]


def match_pattern(filename: str, pattern: str) -> bool:
    """检查文件名是否匹配模式（支持通配符）"""
    # 将通配符转换为正则表达式
    regex_pattern = pattern.replace(".", "\\.").replace("*", ".*").replace("?", ".")
    return bool(re.match(f"^{regex_pattern}$", filename, re.IGNORECASE))


def find_matching_pattern(filename: str, rules: List[PatternRule]) -> Optional[PatternRule]:
    """查找文件匹配的第一个规则"""
    # 按优先级排序
    sorted_rules = sorted(rules, key=lambda r: r.priority)
    for rule in sorted_rules:
        for pattern in rule.patterns:
            if match_pattern(filename, pattern):
                return rule
    return None


def organize_directory(target: str, patterns: List[PatternRule] = None,
                       dry_run: bool = False, delete_empty: bool = True) -> Dict:
    """
    整理目录

    Args:
        target: 目标目录路径
        patterns: 分类规则列表
        dry_run: 预览模式（不实际执行）
        delete_empty: 是否删除空文件夹

    Returns:
        整理结果统计
    """
    target_path = Path(target)
    if not target_path.exists():
        raise FileNotFoundError(f"目录不存在: {target}")

    if patterns is None:
        patterns = DEFAULT_PATTERNS

    # 统计结果
    stats = {
        "total_files": 0,
        "organized": 0,
        "remaining": 0,
        "moves": [],
        "deleted_folders": [],
        "folders_created": []
    }

    # 获取所有文件
    files = [f for f in target_path.iterdir() if f.is_file() and f.name != "desktop.ini"]
    stats["total_files"] = len(files)

    # 创建分类文件夹
    folder_names = set(r.target_folder for r in patterns)
    for folder_name in folder_names:
        folder_path = target_path / folder_name
        if not folder_path.exists():
            if not dry_run:
                folder_path.mkdir(exist_ok=True)
            stats["folders_created"].append(folder_name)

    # 分类文件
    remaining_files = []
    for file in files:
        matched_rule = find_matching_pattern(file.name, patterns)

        if matched_rule:
            target_folder = target_path / matched_rule.target_folder
            target_path_file = target_folder / file.name

            stats["moves"].append({
                "from": str(file),
                "to": str(target_path_file),
                "category": matched_rule.target_folder
            })

            if not dry_run:
                file.rename(target_path_file)
            stats["organized"] += 1
        else:
            remaining_files.append(file)

    stats["remaining"] = len(remaining_files)

    # 删除空文件夹
    if delete_empty and not dry_run:
        for item in target_path.iterdir():
            if item.is_dir() and not any(item.iterdir()):
                item.rmdir()
                stats["deleted_folders"].append(item.name)

    return stats


def print_report(stats: Dict, target: str):
    """打印整理报告"""
    print(f"\n{'='*50}")
    print(f"整理完成: {target}")
    print(f"{'='*50}")
    print(f"总文件数: {stats['total_files']}")
    print(f"已整理: {stats['organized']}")
    print(f"待整理: {stats['remaining']}")

    if stats["folders_created"]:
        print(f"\n新建文件夹: {', '.join(stats['folders_created'])}")

    if stats["deleted_folders"]:
        print(f"删除空文件夹: {', '.join(stats['deleted_folders'])}")

    # 按分类统计
    category_stats = {}
    for move in stats["moves"]:
        cat = move["category"]
        category_stats[cat] = category_stats.get(cat, 0) + 1

    print("\n分类统计:")
    for cat, count in sorted(category_stats.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count} 个文件")

    if stats["moves"]:
        print("\n移动详情:")
        for move in stats["moves"][:10]:  # 只显示前10个
            print(f"  {move['from'].split('/')[-1]} -> {move['category']}/")
        if len(stats["moves"]) > 10:
            print(f"  ... 还有 {len(stats['moves']) - 10} 个文件")


def main():
    parser = argparse.ArgumentParser(description="自动文件整理工具")
    parser.add_argument("--target", "-t", required=True, help="目标目录路径")
    parser.add_argument("--dry-run", "-n", action="store_true", help="预览模式（不执行）")
    parser.add_argument("--config", "-c", help="自定义规则配置文件（JSON）")
    parser.add_argument("--keep-empty", action="store_true", help="不删除空文件夹")

    args = parser.parse_args()

    # 加载自定义规则
    patterns = DEFAULT_PATTERNS
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
            # TODO: 从配置文件加载规则
            print(f"自定义规则功能开发中...")

    try:
        stats = organize_directory(
            target=args.target,
            patterns=patterns,
            dry_run=args.dry_run,
            delete_empty=not args.keep_empty
        )

        if args.dry_run:
            print("【预览模式】以下操作将被执行:")
            print_report(stats, args.target)
        else:
            print_report(stats, args.target)

    except Exception as e:
        print(f"错误: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
