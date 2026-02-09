#!/usr/bin/env python3
"""
文件压缩 Agent
自动检测和压缩文件，保持最小单元结构
"""

import argparse
import gzip
import os
import shutil
import sys
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional


def load_config(dir_path: Path) -> Dict:
    """加载 .compress.md 配置文件"""
    config_path = dir_path / ".compress.md"
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"  [警告] 无法读取配置文件: {e}")
            return {}
    return {}


def should_compress(file_path: Path, config: Dict) -> bool:
    """判断文件是否应该被压缩"""
    # 跳过已经是压缩文件的
    if file_path.suffix == '.gz':
        return False

    # 检查忽略扩展名
    ignore_exts = config.get('ignore_extensions', '.exe,.zip,.gz,.7z,.jpg,.png,.mp4')
    ignore_exts = [e.strip() for e in ignore_exts.split(',')]
    if file_path.suffix.lower() in ignore_exts:
        return False

    # 检查忽略模式
    ignore_patterns = config.get('ignore_patterns', '*temp*,*_backup*,node_modules')
    for pattern in ignore_patterns.split(','):
        pattern = pattern.strip()
        if pattern and file_path.name.lower().find(pattern.lower().replace('*', '')) != -1:
            if '*' in pattern:
                import fnmatch
                if fnmatch.fnmatch(file_path.name, pattern):
                    return False

    # 检查文件大小
    min_size_mb = config.get('min_size_mb', 1)
    file_size_mb = file_path.stat().st_size / (1024 * 1024)
    if file_size_mb < min_size_mb:
        return False

    # 检查修改时间
    max_age_days = config.get('max_age_days', 7)
    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
    if datetime.now() - mtime < timedelta(days=max_age_days):
        return False

    return True


def compress_file(file_path: Path, keep_original: bool = True) -> bool:
    """压缩单个文件为 .gz 格式"""
    try:
        output_path = Path(str(file_path) + '.gz')

        # 如果已存在压缩文件，比较大小决定是否重新压缩
        if output_path.exists():
            original_size = file_path.stat().st_size
            compressed_size = output_path.stat().st_size
            if compressed_size <= original_size * 0.9:  # 只有压缩率 >10% 才更新
                print(f"  跳过: {file_path.name} (已存在更优压缩)")
                return False

        # 执行压缩
        with open(file_path, 'rb') as f_in:
            with gzip.open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        compressed_size_mb = output_path.stat().st_size / (1024 * 1024)
        original_size_mb = file_path.stat().st_size / (1024 * 1024)
        ratio = (1 - compressed_size_mb / original_size_mb) * 100

        print(f"  压缩: {file_path.name}")
        print(f"    原始: {original_size_mb:.2f}MB -> 压缩后: {compressed_size_mb:.2f}MB (节省 {ratio:.1f}%)")

        if not keep_original:
            file_path.unlink()

        return True
    except Exception as e:
        print(f"  [错误] 压缩失败 {file_path}: {e}")
        return False


def scan_directory(target_path: str, config: Dict) -> List[Path]:
    """扫描目录，收集需要压缩的文件"""
    target = Path(target_path)
    files_to_compress = []

    for root, dirs, files in os.walk(target):
        root_path = Path(root)

        # 加载当前目录的配置
        dir_config = load_config(root_path)
        merged_config = {**config, **dir_config}  # 目录级配置优先

        for file in files:
            file_path = root_path / file
            if should_compress(file_path, merged_config):
                files_to_compress.append(file_path)

    return files_to_compress


def update_log(config_path: Path, compressed_files: List[str]):
    """更新压缩日志"""
    if not config_path.exists():
        return

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        content = ""

    log_entry = f"\n## 压缩记录 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n"
    for f in compressed_files:
        log_entry += f"- {f}\n"

    with open(config_path, 'a', encoding='utf-8') as f:
        f.write(log_entry)


def compress_directory(target: str, mode: str = 'preview'):
    """压缩整个目录"""
    target_path = Path(target)
    if not target_path.exists():
        print(f"[错误] 目录不存在: {target}")
        return

    print(f"\n{'='*60}")
    if mode == 'preview':
        print(f"[预览模式] 扫描目录: {target}")
    else:
        print(f"[执行模式] 压缩目录: {target}")
    print(f"{'='*60}\n")

    # 加载根目录配置
    root_config = load_config(target_path)
    keep_original = root_config.get('keep_original', True)

    # 扫描文件
    files_to_compress = scan_directory(target_path, root_config)

    if not files_to_compress:
        print("没有需要压缩的文件。")
        return

    print(f"找到 {len(files_to_compress)} 个可压缩文件:\n")

    if mode == 'preview':
        for f in sorted(files_to_compress):
            size_mb = f.stat().st_size / (1024 * 1024)
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            print(f"  [将压缩] {f.relative_to(target_path.parent)} ({size_mb:.2f}MB, {mtime.strftime('%Y-%m-%d')})")
        print(f"\n共 {len(files_to_compress)} 个文件")
    else:
        # 执行压缩
        compressed = []
        for f in sorted(files_to_compress):
            if compress_file(f, keep_original):
                compressed.append(str(f))

        # 更新日志
        if compressed:
            log_path = target_path / ".compress.md"
            update_log(log_path, compressed)

        print(f"\n完成! 成功压缩 {len(compressed)}/{len(files_to_compress)} 个文件")


def compress_single_file(file_path: str):
    """压缩单个文件"""
    path = Path(file_path)
    if not path.exists():
        print(f"[错误] 文件不存在: {file_path}")
        return

    print(f"\n压缩文件: {path}")
    compress_file(path, keep_original=False)


def main():
    parser = argparse.ArgumentParser(description='文件压缩 Agent')
    parser.add_argument('--target', '-t', help='目标目录路径')
    parser.add_argument('--file', '-f', help='单个文件路径')
    parser.add_argument('--mode', '-m', choices=['preview', 'auto'], default='preview',
                        help='运行模式: preview(预览) 或 auto(执行)')

    args = parser.parse_args()

    if args.file:
        compress_single_file(args.file)
    elif args.target:
        compress_directory(args.target, args.mode)
    else:
        parser.print_help()
        print("\n示例:")
        print("  python compress.py --target C:\\Downloads --mode preview")
        print("  python compress.py --target C:\\Downloads --mode auto")
        print("  python compress.py --file C:\\file.txt")


if __name__ == '__main__':
    main()
