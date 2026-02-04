#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度热搜获取工具
支持：网页解析 + API双通道

注意：百度NLP热点API处于邀测状态，需官方授权
      本工具默认使用网页解析方案
"""

import argparse
import json
import re
import time
import sys
from datetime import datetime
from typing import List, Dict, Optional

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("请安装依赖: pip install requests beautifulsoup4 lxml")
    sys.exit(1)


# 百度热搜榜单分类映射
CATEGORY_MAP = {
    "hot": {"name": "热搜榜", "url": "https://top.baidu.com/board"},
    "domestic": {"name": "国内榜", "url": "https://top.baidu.com/board?category=domestic"},
    "abroad": {"name": "国际榜", "url": "https://top.baidu.com/board?category=abroad"},
    "finance": {"name": "财经榜", "url": "https://top.baidu.com/board?category=finance"},
    "sports": {"name": "体育榜", "url": "https://top.baidu.com/board?category=sports"},
    "entertainment": {"name": "娱乐榜", "url": "https://top.baidu.com/board?category=entertainment"},
    "education": {"name": "教育榜", "url": "https://top.baidu.com/board?category=education"},
    "tech": {"name": "科技榜", "url": "https://top.baidu.com/board?category=tech"},
    "game": {"name": "游戏榜", "url": "https://top.baidu.com/board?category=game"},
    "car": {"name": "汽车榜", "url": "https://top.baidu.com/board?category=car"},
    "estate": {"name": "房产榜", "url": "https://top.baidu.com/board?category=estate"},
    "travel": {"name": "旅游榜", "url": "https://top.baidu.com/board?category=travel"},
}

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}


class BaiduHotSearch:
    """百度热搜获取器"""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def _fetch_page(self, url: str) -> Optional[str]:
        """获取页面HTML"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.encoding = "utf-8"
            return response.text
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None

    def _parse_hot_list(self, html: str, limit: int = 20) -> List[Dict]:
        """解析热搜列表"""
        soup = BeautifulSoup(html, "lxml")
        results = []

        # 方法1: 查找 script 中的 JSON 数据
        scripts = soup.find_all("script")
        for script in scripts:
            text = script.string or ""
            if "feeds" in text or "hotList" in text or "board-data" in text:
                # 尝试提取JSON数据
                json_match = re.search(r'\[.*\]', text, re.DOTALL)
                if json_match:
                    try:
                        data = json.loads(json_match.group())
                        for i, item in enumerate(data[:limit]):
                            results.append({
                                "rank": i + 1,
                                "keyword": item.get("keyword", ""),
                                "heat": item.get("heat", 0),
                                "url": f"https://baidu.com/s?word={item.get('keyword', '')}",
                                "source": "baidu-api"
                            })
                        return results
                    except json.JSONDecodeError:
                        pass

        # 方法2: 解析DOM结构
        items = soup.select(".theme-hot, .list-item, .hot-item, .keyword-item")
        for i, item in enumerate(items[:limit]):
            keyword_elem = item.select_one(".keyword, .title, a")
            heat_elem = item.select_one(".heat, .num, .index")

            keyword = keyword_elem.get_text(strip=True) if keyword_elem else ""
            heat_text = heat_elem.get_text(strip=True) if heat_elem else "0"

            # 提取数字热度
            heat_match = re.search(r'(\d+\.?\d*)', heat_text)
            heat = float(heat_match.group(1)) if heat_match else 0

            if keyword:
                results.append({
                    "rank": i + 1,
                    "keyword": keyword,
                    "heat": heat,
                    "url": f"https://baidu.com/s?word={keyword}",
                    "source": "baidu-html"
                })

        # 方法3: 通用解析（兜底方案）
        if not results:
            all_links = soup.find_all("a", href=re.compile(r'/s\?word='))
            seen = set()
            for i, link in enumerate(all_links[:limit]):
                keyword = link.get_text(strip=True)
                if keyword and keyword not in seen and len(keyword) > 1:
                    seen.add(keyword)
                    results.append({
                        "rank": i + 1,
                        "keyword": keyword,
                        "heat": 0,
                        "url": link.get("href", ""),
                        "source": "baidu-link"
                    })

        return results

    def get_hot_list(self, category: str = "hot", limit: int = 20) -> Dict:
        """获取热搜榜单"""
        if category not in CATEGORY_MAP:
            return {
                "success": False,
                "error": f"不支持的分类: {category}",
                "available_categories": list(CATEGORY_MAP.keys())
            }

        cat_info = CATEGORY_MAP[category]
        url = cat_info["url"]

        print(f"正在获取 {cat_info['name']} ...")

        html = self._fetch_page(url)
        if not html:
            return {
                "success": False,
                "error": "页面获取失败",
                "category": cat_info["name"]
            }

        data = self._parse_hot_list(html, limit)

        if not data:
            return {
                "success": False,
                "error": "数据解析失败，可能页面结构已变化",
                "category": cat_info["name"]
            }

        return {
            "success": True,
            "category": cat_info["name"],
            "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": len(data),
            "data": data
        }

    def search_keyword_trend(self, keyword: str) -> Dict:
        """搜索关键词热度趋势"""
        # 百度指数需要登录，这里提供搜索结果页作为替代
        search_url = f"https://www.baidu.com/s?wd={keyword}"
        return {
            "keyword": keyword,
            "search_url": search_url,
            "note": "完整趋势数据需使用百度指数API（需授权）"
        }


def format_output(data: Dict, output_format: str = "text") -> str:
    """格式化输出"""
    if not data.get("success"):
        return f"错误: {data.get('error', '未知错误')}"

    lines = []
    lines.append(f"【{data['category']}】- {data['fetch_time']}")
    lines.append("-" * 60)

    for item in data["data"]:
        lines.append(f"{item['rank']:2d}. {item['keyword']} (热度: {item['heat']})")
        lines.append(f"    🔗 {item['url']}")

    if output_format == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="百度热搜获取工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python baidu_hot_search.py                          # 获取热搜榜TOP10
  python baidu_hot_search.py --category finance       # 获取财经榜
  python baidu_hot_search.py --limit 20               # 获取TOP20
  python baidu_hot_search.py --format json            # JSON格式输出

可用分类:
  hot(热搜) domestic(国内) abroad(国际) finance(财经)
  sports(体育) entertainment(娱乐) education(教育)
  tech(科技) game(游戏) car(汽车) estate(房产) travel(旅游)
        """
    )

    parser.add_argument("-c", "--category", default="hot",
                        help="榜单分类 (默认: hot)")
    parser.add_argument("-l", "--limit", type=int, default=10,
                        help="获取数量 (默认: 10)")
    parser.add_argument("-f", "--format", default="text",
                        choices=["text", "json"],
                        help="输出格式 (默认: text)")
    parser.add_argument("-o", "--output",
                        help="输出到文件")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="显示详细信息")

    args = parser.parse_args()

    # 初始化获取器
    hot_search = BaiduHotSearch()

    # 获取数据
    result = hot_search.get_hot_list(args.category, args.limit)

    # 输出
    output = format_output(result, args.format)

    if args.verbose:
        output = f"来源: {result.get('source', 'unknown')}\n" + output

    print(output)

    # 保存到文件
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\n已保存到: {args.output}")

    # 返回JSON格式供其他程序使用
    if args.format == "json":
        return result

    return result


if __name__ == "__main__":
    main()
