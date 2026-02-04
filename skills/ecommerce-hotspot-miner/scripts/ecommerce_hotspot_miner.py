#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====================================================================
电商老板热点挖掘机 - 真实数据源版 V2.0
=====================================================================

【经验总结 - 2026-02-03】

## 数据源调研过程

### 可用的免费数据源（按可用性排序）

| 数据源 | 类型 | 可用性 | 备注 |
|:---|:---|:---:|:---|
| 虎嗅网 | 网页抓取 | ✅ 可用 | 财经/科技/商业热点 |
| 36氪 | 网页抓取 | ✅ 可用 | 创业/科技/商业热点 |
| 知乎热榜 | 网页抓取 | ⚠️ 部分可用 | 需要登录 |
| 百度热搜 | 网页抓取 | ❌ 动态页面 | JS渲染，无法直接抓取 |
| 微博热搜 | API | ❌ 403 | 需要登录/频率限制 |
| 今日头条 | 网页抓取 | ❌ 动态页面 | JS渲染 |

### 结论
✅ **可用方案**: 虎嗅网 + 36氪 网页抓取
✅ **备用方案**: 微信公众号文章标题

### 抓取难点
1. 动态页面（百度/头条/微博）：JS渲染，requests无法获取
2. API限制：微博/知乎需要登录/频率限制
3. 反爬虫：部分网站有IP/UA检测

### 解决方案
1. 静态页面优先：虎嗅、36氪首页可抓
2. 解析技巧：BeautifulSoup + 正则
3. 降级方案：使用预设热点词库（当在线不可用时）

=====================================================================
"""

import argparse
import json
import re
import sys
from datetime import datetime
from typing import List, Dict, Optional

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False


# ==================== 电商老板痛点映射表 ====================
"""
【核心经验】将通用热点映射到电商老板痛点的逻辑

为什么需要映射？
- 通用热点（黄金/房价/AI）和老板痛点（利润/流量/成本）之间需要建立关联
- 同一个热点可以从不同角度解读

映射规则：
1. 直接匹配：热点含有关键词 → 直接映射
2. 间接关联：热点主题 → 推导痛点
"""

PAIN_POINT_MAPPING = {
    "利润薄": [
        "赚钱", "盈利", "利润", "亏损", "亏本", "收入", "营收",
        "生意", "订单", "销售额", "GMV", "客单价"
    ],
    "流量贵": [
        "流量", "获客", "推广", "广告", "营销", "曝光",
        "转化", "点击", "询盘", "引流"
    ],
    "成本高": [
        "成本", "费用", "涨价", "价格", "房租", "人工", "工资",
        "租金", "物流", "运费", "原材料", "关税"
    ],
    "转化难": [
        "转化", "销售", "购买", "下单", "成交", "成交率",
        "复购", "留存", "活跃"
    ],
    "平台压榨": [
        "平台", "规则", "抽成", "佣金", "封号", "监管",
        "政策", "合规", "处罚", "限流"
    ],
    "AI焦虑": [
        "AI", "人工智能", "自动化", "智能", "替代", "裁员",
        "智能体", "大模型", "机器人", "无人"
    ],
    "资金压力": [
        "资金", "融资", "贷款", "账期", "回款", "现金流",
        "债务", "违约", "破产", "投资", "募资"
    ],
    "消费降级": [
        "消费", "经济", "降级", "通缩", "省钱", "低价",
        "性价比", "折扣", "便宜"
    ],
}

# 电商相关加权关键词（出现则加权）
ECOMMERCE_KEYWORDS = [
    "电商", "跨境", "零售", "商业", "企业", "老板",
    "商家", "商户", "卖家", "天猫", "淘宝", "京东",
    "拼多多", "亚马逊", "TikTok", "Shopee"
]


class RealHotspotMiner:
    """
    电商老板热点挖掘机

    【使用经验】
    1. 优先抓取虎嗅网（财经产业为主）
    2. 其次36氪（科技创业为主）
    3. 两者的并集覆盖大部分商业热点
    """

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })

    def _fetch_page(self, url: str) -> Optional[str]:
        """通用页面获取"""
        try:
            resp = self.session.get(url, timeout=self.timeout)
            resp.encoding = "utf-8"
            return resp.text
        except Exception as e:
            print(f"请求失败 [{url}]: {e}", file=sys.stderr)
            return None

    def _extract_titles_from_soup(self, html: str, selector: str = "a") -> List[str]:
        """从HTML中提取标题"""
        if not html:
            return []
        soup = BeautifulSoup(html, "html.parser")
        titles = []
        for elem in soup.find_all(selector):
            text = elem.get_text(strip=True)
            if 5 <= len(text) <= 60:
                titles.append(text)
        return titles

    def _calculate_pain_score(self, title: str) -> Dict:
        """
        【核心算法】计算热点与老板痛点的关联度

        评分逻辑：
        - 直接命中痛点关键词：+20-25分
        - 命中电商相关词：+15分
        - 最高100分封顶
        """
        score = 0
        matched_tags = []

        # 痛点匹配
        for pain_point, keywords in PAIN_POINT_MAPPING.items():
            for kw in keywords:
                if kw in title:
                    if pain_point in ["利润薄", "流量贵", "成本高"]:
                        score += 25
                    elif pain_point in ["平台压榨", "资金压力", "AI焦虑"]:
                        score += 22
                    else:
                        score += 15
                    matched_tags.append(pain_point)
                    break

        # 电商加权
        for kw in ECOMMERCE_KEYWORDS:
            if kw in title:
                score += 15
                break

        # 惩罚：非相关内容
        exclude_patterns = ["娱乐", "明星", "八卦", "绯闻", "恋情", "离婚"]
        for p in exclude_patterns:
            if p in title:
                score = max(score - 30, 0)
                break

        return {
            "score": min(score, 100),
            "tags": matched_tags[:3] if matched_tags else ["一般"]
        }

    def mine_huxiu(self, limit: int = 20) -> List[Dict]:
        """
        【数据源1】虎嗅网热点挖掘

        URL: https://www.huxiu.com
        特点：财经、产业、商业分析为主，适合找经济趋势类热点
        """
        url = "https://www.huxiu.com"
        html = self._fetch_page(url)
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        results = []

        # 虎嗅文章链接通常包含 /article/
        for a in soup.find_all("a", href=re.compile(r'/article/\d+')):
            title = a.get_text(strip=True)
            if title and 5 <= len(title) <= 50:
                # 过滤无效标题
                if not any(e in title for e in ["视频", "直播", "专题", "活动", "专栏"]):
                    pain_info = self._calculate_pain_score(title)
                    results.append({
                        "keyword": title,
                        "source": "虎嗅",
                        "url": "https://www.huxiu.com" + a.get("href", ""),
                        **pain_info
                    })

        # 去重
        seen = set()
        unique = []
        for item in results:
            if item["keyword"] not in seen:
                seen.add(item["keyword"])
                unique.append(item)

        return unique[:limit]

    def mine_36kr(self, limit: int = 15) -> List[Dict]:
        """
        【数据源2】36氪热点挖掘

        URL: https://36kr.com/hot-news
        特点：科技、创业、商业为主，适合找AI/科技类热点
        """
        url = "https://36kr.com/hot-news"
        html = self._fetch_page(url)
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        results = []

        # 36氪文章链接通常包含 /p/
        for a in soup.find_all("a", href=re.compile(r'/p/\d+')):
            title = a.get_text(strip=True)
            if title and 5 <= len(title) <= 50:
                pain_info = self._calculate_pain_score(title)
                results.append({
                    "keyword": title,
                    "source": "36氪",
                    "url": "https://36kr.com" + a.get("href", ""),
                    **pain_info
                })

        # 去重
        seen = set()
        unique = []
        for item in results:
            if item["keyword"] not in seen:
                seen.add(item["keyword"])
                unique.append(item)

        return unique[:limit]

    def mine_all(self, limit: int = 20) -> Dict:
        """
        【主入口】聚合所有数据源

        返回格式：
        {
            "success": True,
            "fetch_time": "2026-02-03 20:30:00",
            "sources": ["虎嗅", "36氪"],
            "data": [...]
        }
        """
        huxiu_data = self.mine_huxiu(limit=limit)
        kr36_data = self.mine_36kr(limit=limit)

        all_data = huxiu_data + kr36_data

        if not all_data:
            return {
                "success": False,
                "error": "未能获取到任何热点数据",
                "suggestion": "请检查网络连接或稍后重试"
            }

        # 按分数排序
        all_data.sort(key=lambda x: x["score"], reverse=True)

        return {
            "success": True,
            "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sources": ["虎嗅", "36氪"],
            "total": len(all_data),
            "data": all_data[:limit]
        }

    def analyze_keyword(self, keyword: str) -> Dict:
        """分析任意关键词的痛点关联"""
        pain_info = self._calculate_pain_score(keyword)
        return {
            "keyword": keyword,
            "pain_score": pain_info["score"],
            "tags": pain_info["tags"]
        }


def format_output(data: Dict, user_persona: bool = True) -> str:
    """格式化输出"""
    if not data.get("success"):
        return f"错误: {data.get('error', '未知错误')}\n建议: {data.get('suggestion', '')}"

    lines = []
    lines.append("=" * 70)
    if user_persona:
        lines.append("  电商老板关联热点速递")
        lines.append("  用户画像: [被利润掐住喉咙的老板]")
    else:
        lines.append("  电商热点挖掘结果")
    lines.append("=" * 70)
    lines.append(f"\n⏰ {data['fetch_time']}")
    lines.append(f"📡 数据来源: {', '.join(data['sources'])}")
    lines.append("-" * 70)

    for i, item in enumerate(data.get("data", []), 1):
        tags = item.get("tags", [])[:2]
        score = item.get("score", 0)
        bars = "█" * (score // 10) + "░" * (10 - score // 10)
        lines.append(f"\n{i:2d}. {item['keyword']}")
        lines.append(f"    来源: {item['source']}")
        lines.append(f"    关联痛点: {', '.join(tags) if tags else '一般'}")
        lines.append(f"    相关度: {bars} {score}分")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="电商老板热点挖掘机 - 真实数据源",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
【使用经验】
数据源：
  - 虎嗅网 (https://www.huxiu.com) → 财经/产业/商业
  - 36氪 (https://36kr.com/hot-news) → 科技/创业/商业

示例：
  python ecommerce_hotspot_miner.py              # 获取全部热点
  python ecommerce_hotspot_miner.py --limit 10   # TOP10
  python ecommerce_hotspot_miner.py --json        # JSON格式
  python ecommerce_hotspot_miner.py -a "光伏"     # 分析关键词

注意事项：
  - 百度热搜/微博热搜需要登录，无法直接抓取
  - 如遇网络问题，会返回空数据
        """
    )

    parser.add_argument("-l", "--limit", type=int, default=20,
                        help="返回数量")
    parser.add_argument("-f", "--format", default="text",
                        choices=["text", "json"],
                        help="输出格式")
    parser.add_argument("-o", "--output",
                        help="输出到文件")
    parser.add_argument("-a", "--analyze",
                        help="分析单个关键词")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="简洁模式（不显示用户画像）")

    args = parser.parse_args()

    if not HAS_DEPS:
        print("请安装依赖: pip install requests beautifulsoup4")
        sys.exit(1)

    miner = RealHotspotMiner()

    # 分析关键词模式
    if args.analyze:
        result = miner.analyze_keyword(args.analyze)
        output = json.dumps(result, ensure_ascii=False, indent=2)
        print(output)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
        return

    # 正常获取
    result = miner.mine_all(limit=args.limit)

    if args.format == "json":
        output = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        output = format_output(result, not args.quiet)

    print(output)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\n已保存到: {args.output}")


if __name__ == "__main__":
    main()
