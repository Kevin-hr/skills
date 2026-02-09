# Auto Organize Scripts

## 分类标准 (Strict Attribute-Based Classification)

### 核心原则
- **同类型文件放同类型文件夹**
- **文件夹名清晰无歧义**
- **一个文件夹只存在一种属性类型的文件**
- **跳过系统文件(.AppData, .config等)和正在运行的程序文件**
- **资源文件夹扁平化** - 打开即文件，无嵌套
- **最小颗粒度** - 递归清理直到无子文件夹

### 文件夹命名规范

| 文件夹 | 包含类型 | 示例 |
|--------|----------|------|
| `Images/` | 图片文件 | png, jpg, jpeg, gif, webp, svg, jfif |
| `Videos/` | 视频文件 | mp4, mov, avi, mkv, webm |
| `Audio/` | 音频文件 | mp3, wav, flac, aac, ogg |
| `Documents/` | 办公文档 | docx, xls, xlsx, ppt, pptx, txt |
| `Data/` | 数据文件 | csv, html, json (纯数据), md (说明文档) |
| `PDFs/` | PDF文档 | pdf |
| `Archives/` | 压缩档案/杂项 | zip, rar, 7z, tar, gz, lnk, log |
| `Installers/` | 安装包 | exe, dmg, pkg, deb, apk |
| `Workflows/` | 工作流配置 | json, yaml, yml |
| `Unsorted/` | 待分类 | 临时存放未知类型 |

### 平台特定分类 (Social Media Patterns)

| 平台 | 文件特征 | 目标文件夹 |
|------|----------|------------|
| 微信 | wx_*.png, *2025*.jpg | WeChat/ |
| 小红书 | *小红书*.jpg, 1083.jpeg | XiaoHongShu/ |
| 抖音 | *抖音*.mp4, 抖音*.png | 社媒发布/ |
| AI资源 | *雲帆*.png, fJ8*.jpeg, AI*.png | AI-Resources/ |
| 封面图 | *封面*.png, *爆款*.png | Covers/ |

### macOS 清理规则

```bash
# 删除 macOS 资源分叉文件夹
rm -rf __MACOSX

# 删除 ._ 前缀文件
rm -f ._*
```

### 整理命令

```bash
# 创建分类文件夹
mkdir -p Images Videos Audio Documents PDFs Installers Archives Workflows Unsorted

# 移动图片
mv *.png *.jpg *.jpeg *.gif *.webp *.svg *.jfif Images/

# 移动视频
mv *.mp4 *.mov *.avi *.mkv *.webm Videos/

# 移动文档
mv *.docx *.xls *.xlsx *.ppt *.pptx *.txt Documents/

# 移动数据文件
mv *.csv *.html *.md Data/

# 移动PDF
mv *.pdf PDFs/

# 移动安装包
mv *.exe *.dmg *.pkg *.deb *.apk Installers/

# 移动压缩包
mv *.zip *.rar *.7z *.tar *.gz Archives/

# 移动工作流配置
mv *.json *.yaml *.yml Workflows/

# 清理 macOS 残留
rm -rf __MACOSX ._*
```

### 深度清理命令 (扁平化)

```bash
# 1. 查找所有嵌套文件夹
find /path -maxdepth 3 -type d

# 2. 递归移动子文件夹内容到父文件夹
mv /path/parent/child/* /path/parent/ 2>/dev/null

# 3. 删除空子文件夹
rmdir /path/parent/child 2>/dev/null

# 4. 删除系统缓存文件夹
rm -rf /path/*/QQMusicCache /path/*/QQPCMgr /path/*/DiskGenius /path/*/AppData /path/*/Temp

# 5. 删除临时文件
rm -f /path/*/~$* /path/*/.log /path/*/.tmp

# 6. 验证扁平化
find /path -maxdepth 2 -type d | head -20
```

### 清理清单

| 类型 | 目标 | 命令 |
|------|------|------|
| 系统缓存 | 删除 | `QQMusicCache`, `QQPCMgr`, `DiskGenius`, `AppData`, `Temp` |
| 临时文件 | 删除 | `~$*`, `*.log`, `*.tmp`, `.DS_Store` |
| macOS残留 | 删除 | `__MACOSX`, `._*` |
| 空文件夹 | 删除 | `rmdir <folder>` |

### auto_organize.py

自动化文件整理脚本，支持预览模式和自定义规则。

### 使用方法

```bash
# 预览模式（不实际执行）
python scripts/auto_organize.py --target /path/to/folder --dry-run

# 执行整理
python scripts/auto_organize.py --target /path/to/folder

# 保留空文件夹
python scripts/auto_organize.py --target /path --keep-empty
```

### 输出示例

```
==================================================
整理完成: C:/Users/52648/Pictures
==================================================
总文件数: 19
已整理: 17
待整理: 2

新建文件夹: WeChat, XiaoHongShu, Covers, AI-Resources

分类统计:
  WeChat: 5 个文件
  AI-Resources: 5 个文件
  XiaoHongShu: 4 个文件
  Covers: 4 个文件
```

### 快速命令

```bash
# 整理 Pictures（完整命令）
cd /c/Users/52648/Pictures && python /c/Users/52648/.agents/skills/file-organizer/scripts/auto_organize.py --target .

# 整理 Downloads
python /c/Users/52648/.agents/skills/file-organizer/scripts/auto_organize.py --target /c/Users/52648/Downloads
```
