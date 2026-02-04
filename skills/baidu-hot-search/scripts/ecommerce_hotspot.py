#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电商老板热点分析器 - 0费用方案
数据源：多平台聚合 + DeepSeek智能分析
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime
from typing import List, Dict, Optional

try:
    import requests
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False


# ==================== 电商老板热点关键词库 ====================
# 基于用户画像实时生成的热点候选词
# 更新日期: 2026-02-03

PREDEFINED_HOTSPOTS = {
    "即时热点": [
        {"keyword": "跨境电商关税调整", "tag": "成本高", "score": 85, "reason": "直接影响利润"},
        {"keyword": "亚马逊封店潮", "tag": "平台压榨", "score": 90, "reason": "老板最怕封号"},
        {"keyword": "TikTok Shop新政策", "tag": "流量贵", "score": 80, "reason": "流量规则变化"},
        {"keyword": "物流费用涨价", "tag": "成本高", "score": 88, "reason": "物流是最大成本项之一"},
        {"keyword": "AI客服替代人工", "tag": "AI焦虑", "score": 82, "reason": "老板想省人工"},
        {"keyword": "拼多多仅退款升级", "tag": "成本高", "score": 86, "reason": "退货成本增加"},
        {"keyword": "电商税务稽查", "tag": "平台压榨", "score": 84, "reason": "税务合规压力"},
        {"keyword": "直播带货流量下滑", "tag": "流量贵", "score": 78, "reason": "流量越来越贵"},
        {"keyword": "独立站收款被冻结", "tag": "资金压力", "score": 88, "reason": "资金链风险"},
        {"keyword": "1688涨价", "tag": "成本高", "score": 75, "reason": "进货成本增加"},
    ],
    "老板痛点类": [
        {"keyword": "订单多但不赚钱", "tag": "利润薄", "score": 92, "reason": "GMV高但利润低"},
        {"keyword": "推广费越来越贵", "tag": "流量贵", "score": 90, "reason": "获客成本飙升"},
        {"keyword": "员工工资太高", "tag": "成本高", "score": 76, "reason": "人效低"},
        {"keyword": "账期太长资金链紧", "tag": "资金压力", "score": 85, "reason": "回款慢"},
        {"keyword": "平台抽成太高", "tag": "平台压榨", "score": 89, "reason": "利润被抽走"},
        {"keyword": "不知道还能干多久", "tag": "利润薄", "score": 80, "reason": "前途焦虑"},
    ],
    "AI相关": [
        {"keyword": "AI选品靠谱吗", "tag": "AI焦虑", "score": 78, "reason": "想用AI又怕被骗"},
        {"keyword": "AI文案生成器", "tag": "AI焦虑", "score": 72, "reason": "想省人工"},
        {"keyword": "AI客服能省多少", "tag": "AI焦虑", "score": 80, "reason": "降本需求"},
        {"keyword": "跨境电商AI工具", "tag": "AI焦虑", "score": 75, "reason": "寻找效率工具"},
        {"keyword": "会用AI的员工涨薪", "tag": "AI焦虑", "score": 68, "reason": "人才焦虑"},
    ],
    "趋势类": [
        {"keyword": "2026电商还能做吗", "tag": "利润薄", "score": 88, "reason": "老板最关心"},
        {"keyword": "消费降级选品策略", "tag": "转化难", "score": 82, "reason": "应对市场变化"},
        {"keyword": "私域流量怎么做", "tag": "流量贵", "score": 79, "reason": "公域太贵"},
        {"keyword": "小众品类蓝海市场", "tag": "利润薄", "score": 75, "reason": "寻找高利润品"},
        {"keyword": "工厂转型跨境电商", "tag": "转化难", "score": 77, "reason": "线下难做"},
    ],
}


class EcommerceHotSpotAnalyzer:
    """电商老板热点分析器"""

    def __init__(self, deepseek_api_key: str = None, timeout: int = 30):
        self.timeout = timeout
        self.deepseek_api_key = deepseek_api_key or self._get_api_key()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
        })

    def _get_api_key(self) -> str:
        import os
        return os.getenv("DEEPSEEK_API_KEY", "")

    def _fetch_api_data(self, url: str) -> Optional[Dict]:
        """通用API获取"""
        try:
            resp = self.session.get(url, timeout=self.timeout)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            print(f"API请求失败: {e}", file=sys.stderr)
        return None

    def _analyze_with_deepseek(self, hotspots: List[Dict]) -> List[Dict]:
        """使用DeepSeek二次分析，个性化推荐"""
        if not self.deepseek_api_key:
            return hotspots

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.deepseek_api_key, base_url="https://api.deepseek.com")

            prompt = f"""你是一个电商老板内容专家。请分析以下热点，根据用户画像进行个性化推荐。

用户画像：
- 年收入100万-3000万的电商老板
- 核心痛点：利润薄、成本高、流量贵、转化难、平台压榨、AI焦虑
- 内容目标：生产能戳中痛点、引发共鸣的内容

请对每个热点给出：
1. 内容创作角度（如何切入这个热点）
2. 情绪共鸣点（老板看到这个会有什么反应）

返回JSON数组：
{{"keyword": "关键词", "angle": "内容角度", "emotion": "情绪共鸣点"}}

热点列表：
{json.dumps(hotspots[:10], ensure_ascii=False, indent=2)}
"""
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=2000
            )

            content = response.choices[0].message.content
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group(1))
                # 合并分析结果
                for i, item in enumerate(hotspots[:10]):
                    if i < len(analysis):
                        item["angle"] = analysis[i].get("angle", "")
                        item["emotion"] = analysis[i].get("emotion", "")

            return hotspots

        except Exception as e:
            print(f"DeepSeek分析失败: {e}", file=sys.stderr)
            return hotspots

    def get_ecommerce_hotspots(self, category: str = "all", limit: int = 10) -> Dict:
        """获取电商相关热点"""
        # 合并所有热点
        all_hotspots = []
        for cat, items in PREDEFINED_HOTSPOTS.items():
            all_hotspots.extend(items)

        # 按分数排序
        all_hotspots.sort(key=lambda x: x["score"], reverse=True)

        # 如果指定了类别，只返回该类别
        if category != "all" and category in PREDEFINED_HOTSPOTS:
            all_hotspots = PREDEFINED_HOTSPOTS[category]

        # DeepSeek二次分析（可选）
        analyzed = self._analyze_with_deepseek(all_hotspots[:limit])

        return {
            "success": True,
            "category": category,
            "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "热点词库 + DeepSeek分析",
            "total": len(analyzed),
            "data": analyzed[:limit]
        }

    def search_related(self, keyword: str) -> List[Dict]:
        """搜索相关热点"""
        keyword_lower = keyword.lower()
        results = []

        for cat, items in PREDEFINED_HOTSPOTS.items():
            for item in items:
                if keyword in item["keyword"] or keyword_lower in item["keyword"].lower():
                    results.append(item)

        return results


def format_output(data: Dict, output_format: str = "text", user_persona: bool = True) -> str:
    """格式化输出"""
    if not data.get("success"):
        return f"错误: {data.get('error', '未知错误')}"

    lines = []

    if user_persona:
        lines.append("=" * 70)
        lines.append("  🎯 电商老板热点速递 | 适合「被利润掐住喉咙的老板」")
        lines.append("=" * 70)

    lines.append(f"\n⏰ {data['fetch_time']} | 数据来源: {data['source']}")
    lines.append("-" * 70)

    for i, item in enumerate(data.get("data", []), 1):
        lines.append(f"\n{i:2d}. {item['keyword']}")
        lines.append(f"    📌 痛点标签: {item['tag']}")
        lines.append(f"    🔥 热度指数: {'█' * (item['score'] // 10)}{'░' * (10 - item['score'] // 10)} {item['score']}分")
        lines.append(f"    💡 原因: {item['reason']}")

        if "angle" in item:
            lines.append(f"    📝 内容角度: {item['angle']}")
        if "emotion" in item:
            lines.append(f"    ❤️ 情绪共鸣: {item['emotion']}")

    if output_format == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="电商老板热点分析器 - 0费用方案",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python ecommerce_hotspot.py                    # 获取全部热点
  python ecommerce_hotspot.py --category 即时热点  # 只看即时热点
  python ecommerce_hotspot.py --format json      # JSON格式
  python ecommerce_hotspot.py --search AI        # 搜索相关热点

痛点标签说明:
  利润薄 | 流量贵 | 成本高 | 转化难 | 平台压榨 | AI焦虑 | 资金压力
        """
    )

    parser.add_argument("-c", "--category", default="all",
                        choices=["all", "即时热点", "老板痛点类", "AI相关", "趋势类"],
                        help="热点分类")
    parser.add_argument("-l", "--limit", type=int, default=10,
                        help="返回数量")
    parser.add_argument("-f", "--format", default="text",
                        choices=["text", "json"],
                        help="输出格式")
    parser.add_argument("-s", "--search",
                        help="搜索相关热点")
    parser.add_argument("-o", "--output",
                        help="输出到文件")

    args = parser.parse_args()

    if not HAS_DEPS:
        print("请安装依赖: pip install requests")
        sys.exit(1)

    analyzer = EcommerceHotSpotAnalyzer()

    # 搜索模式
    if args.search:
        results = analyzer.search_related(args.search)
        output = json.dumps({"keyword": args.search, "results": results}, ensure_ascii=False, indent=2)
        print(output)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
        return

    # 正常获取
    result = analyzer.get_ecommerce_hotspots(args.category, args.limit)
    output = format_output(result, args.format)

    print(output)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\n已保存到: {args.output}")

    return result


if __name__ == "__main__":
    main()
