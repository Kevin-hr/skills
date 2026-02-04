#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实热点获取器 - 0费用方案
数据源：虎嗅网 + 36氪 + 微博热搜(备用)
"""

import argparse
import json
import re
import sys
from datetime import datetime
from typing import List, Dict, Optional

try:
    import requests
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False


# ==================== 电商老板痛点映射表 ====================
# 将通用热点映射到老板痛点

PAIN_POINT_MAPPING = {
    "利润薄": ["赚钱", "盈利", "利润", "亏损", "亏本", "收入", "营收", "生意", "订单"],
    "流量贵": ["流量", "获客", "推广", "广告", "营销", "曝光"],
    "成本高": ["成本", "费用", "涨价", "价格", "房租", "人工", "工资", "租金"],
    "转化难": ["转化", "销售", "购买", "下单", "成交"],
    "平台压榨": ["平台", "规则", "抽成", "佣金", "封号", "监管"],
    "AI焦虑": ["AI", "人工智能", "自动化", "智能", "替代", "裁员"],
    "资金压力": ["资金", "融资", "贷款", "账期", "回款", "现金流", "债务"],
    "消费降级": ["消费", "经济", "降级", "通缩", "省钱"],
}


class RealHotSpotAnalyzer:
    """真实热点分析器"""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })

    def _fetch_page(self, url: str) -> Optional[str]:
        """获取页面HTML"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.encoding = "utf-8"
            return response.text
        except Exception as e:
            print(f"请求失败: {e}", file=sys.stderr)
            return None

    def _map_to_ecommerce_pain(self, title: str) -> List[str]:
        """将热点映射到电商老板痛点"""
        tags = []
        for pain_point, keywords in PAIN_POINT_MAPPING.items():
            for kw in keywords:
                if kw in title:
                    tags.append(pain_point)
                    break
        if not tags:
            tags = ["一般热点"]
        return tags

    def _extract_from_huxiu(self) -> List[Dict]:
        """从虎嗅网获取真实热点"""
        try:
            url = "https://www.huxiu.com"
            html = self._fetch_page(url)
            if not html:
                return []

            # 解析热点文章标题
            soup = BeautifulSoup(html, "html.parser")
            articles = []

            # 查找文章标题
            for a in soup.find_all("a", href=re.compile(r'/article/\d+')):
                title = a.get_text(strip=True)
                if title and 5 <= len(title) <= 50:
                    # 过滤非热点类
                    exclude = ["视频", "直播", "专题", "专栏", "活动"]
                    if not any(e in title for e in exclude):
                        articles.append({
                            "keyword": title,
                            "source": "虎嗅",
                            "tags": self._map_to_ecommerce_pain(title),
                            "url": "https://www.huxiu.com" + a.get("href", "")
                        })

            # 去重
            seen = set()
            unique = []
            for art in articles:
                if art["keyword"] not in seen:
                    seen.add(art["keyword"])
                    unique.append(art)

            return unique[:20]

        except Exception as e:
            print(f"虎嗅解析失败: {e}", file=sys.stderr)
            return []

    def _get_36kr_hot(self) -> List[Dict]:
        """从36氪获取真实热点"""
        try:
            url = "https://36kr.com/hot-news"
            html = self._fetch_page(url)
            if not html:
                return []

            soup = BeautifulSoup(html, "html.parser")
            articles = []

            for a in soup.find_all("a", href=re.compile(r'/p/\d+')):
                title = a.get_text(strip=True)
                if title and 5 <= len(title) <= 50:
                    articles.append({
                        "keyword": title,
                        "source": "36氪",
                        "tags": self._map_to_ecommerce_pain(title),
                        "url": "https://36kr.com" + a.get("href", "")
                    })

            # 去重
            seen = set()
            unique = []
            for art in articles:
                if art["keyword"] not in seen:
                    seen.add(art["keyword"])
                    unique.append(art)

            return unique[:15]

        except Exception as e:
            print(f"36氪解析失败: {e}", file=sys.stderr)
            return []

    def get_ecommerce_hotspots(self, limit: int = 15) -> Dict:
        """获取电商相关热点"""
        # 获取多个数据源
        huxiu_data = self._extract_from_huxiu()
        kr36_data = self._get_36kr_hot()

        # 合并
        all_data = huxiu_data + kr36_data

        if not all_data:
            return {
                "success": False,
                "error": "未能获取到任何热点数据",
                "suggestion": "请检查网络连接或稍后重试"
            }

        # 标记痛点并评分
        scored = []
        for item in all_data:
            pain_score = 0
            for tag in item.get("tags", []):
                if tag in ["利润薄", "流量贵", "成本高"]:
                    pain_score += 25
                elif tag in ["平台压榨", "资金压力", "AI焦虑"]:
                    pain_score += 20
                elif tag in ["转化难", "消费降级"]:
                    pain_score += 15

            # 电商相关关键词加权
            ecommerce_keywords = ["电商", "跨境", "消费", "零售", "商业", "企业", "老板", "平台"]
            for kw in ecommerce_keywords:
                if kw in item["keyword"]:
                    pain_score += 15
                    break

            scored.append({
                **item,
                "pain_score": min(pain_score, 100)
            })

        # 按痛点分数排序
        scored.sort(key=lambda x: x["pain_score"], reverse=True)

        return {
            "success": True,
            "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sources": ["虎嗅", "36氪"],
            "total": len(scored),
            "data": scored[:limit]
        }


def format_output(data: Dict) -> str:
    """格式化输出"""
    if not data.get("success"):
        return f"错误: {data.get('error', '未知错误')}\n建议: {data.get('suggestion', '')}"

    lines = []
    lines.append("=" * 70)
    lines.append("  电商老板关联热点速递")
    lines.append("  用户画像: [被利润掐住喉咙的老板]")
    lines.append("=" * 70)
    lines.append(f"\n⏰ {data['fetch_time']}")
    lines.append(f"📡 数据来源: {', '.join(data['sources'])}")
    lines.append("-" * 70)

    for i, item in enumerate(data.get("data", []), 1):
        tags = item.get("tags", [])[:2]
        lines.append(f"\n{i:2d}. {item['keyword']}")
        lines.append(f"    来源: {item['source']}")
        lines.append(f"    关联痛点: {', '.join(tags) if tags else '一般'}")
        lines.append(f"    相关度: {'█' * (item['pain_score'] // 10)}{'░' * (10 - item['pain_score'] // 10)} {item['pain_score']}分")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="电商老板热点分析器 - 真实数据源",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("-l", "--limit", type=int, default=15,
                        help="返回数量")
    parser.add_argument("-f", "--format", default="text",
                        choices=["text", "json"],
                        help="输出格式")
    parser.add_argument("-o", "--output",
                        help="输出到文件")

    args = parser.parse_args()

    if not HAS_DEPS:
        print("请安装依赖: pip install requests beautifulsoup4 lxml")
        sys.exit(1)

    analyzer = RealHotSpotAnalyzer()
    result = analyzer.get_ecommerce_hotspots(args.limit)

    output = format_output(result)
    if args.format == "json":
        output = json.dumps(result, ensure_ascii=False, indent=2)

    print(output)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\n已保存到: {args.output}")


if __name__ == "__main__":
    main()
