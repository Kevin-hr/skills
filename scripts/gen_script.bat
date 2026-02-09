#!/bin/bash
# 雲帆AI脚本生成器 CLI

# 切换到脚本目录
cd "$(dirname "$0")"

# 运行Python脚本，传递所有参数
python yunfan_script_gen.py "$@"
