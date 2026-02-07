"""
雲帆AI爆款脚本自动生成器
基于5大核心原则 + 金枪大叔公式 + V2.0专业分镜标准
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum
import json
import re


class ScriptTemplate(Enum):
    """脚本模板类型"""
    TOOL_REVIEW = "tool_review"       # AI工具测评
    MONEY_CASE = "money_case"        # AI变现案例
    WORKFLOW = "workflow"            # AI工作流
    HOT解读 = "hot_analysis"          # AI热点解读


class HookType(Enum):
    """钩子类型"""
    CONFLICT = "conflict"            # 冲突式
    NUMERIC = "numeric"              # 数字式
    SUSPENSE = "suspense"            # 悬念式
    QUESTION = "question"            # 提问式
    COMPARISON = "comparison"        # 对比式
    EMOTION = "emotion"              # 情绪式


@dataclass
class Scene:
    """单个分镜"""
    scene_id: int
    duration: float          # 秒
    content: str            # 画面描述
    narration: str          # 旁白/台词
    visual_style: str       # 视觉风格
    transition: str = "cut"  # 转场方式


@dataclass
class Script:
    """完整脚本"""
    script_id: str
    template_type: str
    topic: str
    hook_type: str
    total_duration: float
    scenes: List[Scene]
    core_principles: List[str]  # 应用的核心原则
    cta: str                    # 行动指令

    def to_dict(self) -> Dict:
        return {
            "script_id": self.script_id,
            "template_type": self.template_type,
            "topic": self.topic,
            "hook_type": self.hook_type,
            "total_duration": self.total_duration,
            "scene_count": len(self.scenes),
            "scenes": [asdict(s) for s in self.scenes],
            "core_principles": self.core_principles,
            "cta": self.cta
        }


@dataclass
class ScriptConfig:
    """脚本生成配置"""
    template: ScriptTemplate = ScriptTemplate.TOOL_REVIEW
    hook_type: HookType = HookType.CONFLICT
    target_duration: float = 90.0    # 目标时长(秒)
    target_shots_per_minute: float = 28.0  # 每分钟分镜数
    language: str = "zh-CN"


class YunfanScriptGenerator:
    """雲帆AI脚本生成器"""

    # 钩子库
    HOOKS = {
        HookType.CONFLICT: [
            "别再用{old_tool}了！这个{AI_tool}免费还更强",
            "还在花冤枉钱？{AI_tool}不花钱效果更好",
            "放弃{manual_work}吧，AI让你告别加班",
        ],
        HookType.NUMERIC: [
            "用这个方法，我{days}天赚了{amount}",
            "{people}个人里，只有{count}个知道这个方法",
            "这套工作流让我效率提升{ratio}倍",
        ],
        HookType.SUSPENSE: [
            "{topic}的真相，{percent}%的人不知道",
            "{hot_event}背后，藏着一个小秘密",
            "关于{AI_tool}，你可能被忽悠了",
        ],
        HookType.QUESTION: [
            "你还在花钱{action}？",
            "为什么{AI_tool}没人用？",
            "如果{AI_tool}能{benefit}，你会用吗？",
        ],
        HookType.COMPARISON: [
            "手工 vs AI，差距太大了",
            "{tool1}和{AI_tool}对比，结果我惊了",
            "同样是{AI_tool}，为什么有人用它赚钱",
        ],
        HookType.EMOTION: [
            "终于有人把这个说清楚了",
            "看完这篇，你会感谢自己",
            "这个{AI_tool}让我少走3年弯路",
        ]
    }

    # CTA话术库
    CTAS = {
        "tool_review": [
            "想要{tool_name}工具包的，评论区扣1",
            "需要{tool_name}安装包的，关注后私信我",
            "这么多好用的AI工具，想要的评论区举个手",
        ],
        "money_case": [
            "想学的点关注，私信【变现】",
            "这套方法我整理成了教程，想要的私信",
            "想一起搞钱的，评论区扣【一起】",
        ],
        "workflow": [
            "要工作流模板的，评论区扣【模板】",
            "完整工作流已整理好，需要的关注后私信",
            "想要同款效率提升的，评论区666",
        ],
        "hot_analysis": [
            "关注后私信【资料】领取全套",
            "这套资料我整理好了，想要的评论区扣1",
            "更多干货关注我，持续更新中",
        ]
    }

    def __init__(self, config: Optional[ScriptConfig] = None):
        self.config = config or ScriptConfig()

    def generate(self, topic: str, **kwargs) -> Script:
        """生成脚本"""
        # 根据模板类型生成不同结构的脚本
        template_handlers = {
            ScriptTemplate.TOOL_REVIEW: self._gen_tool_review,
            ScriptTemplate.MONEY_CASE: self._gen_money_case,
            ScriptTemplate.WORKFLOW: self._gen_workflow,
            ScriptTemplate.HOT解读: self._gen_hot_analysis,
        }

        handler = template_handlers.get(self.config.template, self._gen_tool_review)
        return handler(topic, **kwargs)

    def _gen_tool_review(self, topic: str, old_tool: str = "传统工具",
                         ai_tool: str = "AI工具", tool_name: str = "工具包", **kwargs) -> Script:
        """生成AI工具测评脚本"""
        hook = self._gen_hook(topic, old_tool=old_tool, AI_tool=ai_tool)

        scenes = [
            Scene(1, 3.0, f"大字标题：{hook[:25]}", f"开场白：{hook[:20]}", "冲击文字"),
            Scene(2, 12.0, "痛点场景：{old_tool}".format(old_tool=old_tool),
                  "还在用{old_tool}？效率低还费钱".format(old_tool=old_tool), "情景再现"),
            Scene(3, 45.0, "AI工具界面演示",
                  "看这个{AI_tool}，功能A对比演示".format(AI_tool=ai_tool), "屏幕录制"),
            Scene(4, 30.0, "效果对比图",
                  "对比一下，效果差距明显", "分屏对比"),
            Scene(5, 10.0, "推荐总结 + CTA",
                  "推荐{tool_name}，评论区扣1".format(tool_name=tool_name), "产品展示"),
        ]

        return Script(
            script_id=f"sr_{self._gen_id()}",
            template_type="tool_review",
            topic=topic,
            hook_type=self.config.hook_type.value,
            total_duration=sum(s.duration for s in scenes),
            scenes=scenes,
            core_principles=["有用性", "开头承诺", "AI对比"],
            cta=self._gen_cta("tool_review", tool_name=tool_name)
        )

    def _gen_money_case(self, topic: str, days: str = "3天", amount: str = "5000",
                        people: str = "10个人", count: str = "1个", **kwargs) -> Script:
        """生成AI变现案例脚本"""
        hook = self._gen_hook(topic, days=days, amount=amount, people=people, count=count)

        scenes = [
            Scene(1, 3.0, "收益截图大字展示", "她用AI做副业月入{amount}".format(amount=amount), "数据展示"),
            Scene(2, 17.0, "痛点共鸣场景", "很多人觉得AI离钱很远，其实...", "情景对话"),
            Scene(3, 40.0, "案例操作演示",
                  "具体步骤：第一步...第二步...第三步...", "教程演示"),
            Scene(4, 20.0, "底层逻辑讲解", "为什么她能成功？因为...", "口播讲解"),
            Scene(5, 10.0, "价值承诺 + CTA", "这套方法我整理好了", "人物出镜"),
        ]

        return Script(
            script_id=f"mc_{self._gen_id()}",
            template_type="money_case",
            topic=topic,
            hook_type=self.config.hook_type.value,
            total_duration=sum(s.duration for s in scenes),
            scenes=scenes,
            core_principles=["有用性", "底层逻辑", "开头承诺", "情绪钩子"],
            cta=self._gen_cta("money_case")
        )

    def _gen_workflow(self, topic: str, ratio: str = "10", **kwargs) -> Script:
        """生成AI工作流脚本"""
        hook = self._gen_hook(topic, ratio=ratio)

        scenes = [
            Scene(1, 3.0, "效率对比大字", "这个工作流让我效率提升{ratio}倍".format(ratio=ratio), "冲击画面"),
            Scene(2, 12.0, "痛点场景：加班", "手工做{topic}太慢了", "情景再现"),
            Scene(3, 35.0, "AI工作流全流程演示", "看好了，三步搞定", "屏幕录制"),
            Scene(4, 20.0, "价值量化", "省下多少时间多少钱", "数据展示"),
            Scene(5, 15.0, "进阶版预告 + CTA", "要工作流模板的评论区扣【模板】", "产品展示"),
        ]

        return Script(
            script_id=f"wf_{self._gen_id()}",
            template_type="workflow",
            topic=topic,
            hook_type=self.config.hook_type.value,
            total_duration=sum(s.duration for s in scenes),
            scenes=scenes,
            core_principles=["有用性", "热点入口", "开头承诺"],
            cta=self._gen_cta("workflow")
        )

    def _gen_hot_analysis(self, topic: str, hot_event: str = "XX事件",
                          percent: str = "90", **kwargs) -> Script:
        """生成AI热点解读脚本"""
        hook = self._gen_hook(topic, hot_event=hot_event, percent=percent)

        scenes = [
            Scene(1, 3.0, "热点话题大字", "{hook}".format(hook=hook[:20]), "冲击文字"),
            Scene(2, 17.0, "热点事件回顾", "{hot_event}始末，一文说清".format(hot_event=hot_event), "新闻混剪"),
            Scene(3, 30.0, "深度分析", "底层逻辑是什么？", "口播讲解"),
            Scene(4, 20.0, "机会解读", "普通人如何抓住这波机会", "案例展示"),
            Scene(5, 15.0, "资料领取 + CTA", "关注后私信【资料】", "二维码展示"),
        ]

        return Script(
            script_id=f"ha_{self._gen_id()}",
            template_type="hot_analysis",
            topic=topic,
            hook_type=self.config.hook_type.value,
            total_duration=sum(s.duration for s in scenes),
            scenes=scenes,
            core_principles=["热点入口", "底层逻辑", "有用性", "情绪钩子"],
            cta=self._gen_cta("hot_analysis")
        )

    def _gen_hook(self, topic: str, **kwargs) -> str:
        """生成开场钩子"""
        hooks = self.HOOKS.get(self.config.hook_type, self.HOOKS[HookType.CONFLICT])
        hook_template = hooks[0]  # 取第一个模板

        # 替换占位符（不使用**kwargs避免重复）
        result = hook_template.format(
            topic=topic,
            manual_work=f"手工{topic}",
            AI_tool=kwargs.get("AI_tool", "AI工具"),
            old_tool=kwargs.get("old_tool", "传统工具"),
            days=kwargs.get("days", "3天"),
            amount=kwargs.get("amount", "5000"),
            ratio=kwargs.get("ratio", "10"),
            people=kwargs.get("people", "10个人"),
            count=kwargs.get("count", "1个"),
            percent=kwargs.get("percent", "90"),
            hot_event=kwargs.get("hot_event", topic)
        )
        return result

    def _gen_cta(self, template_type: str, **kwargs) -> str:
        """生成CTA"""
        cta_list = self.CTAS.get(template_type, self.CTAS["tool_review"])
        cta_template = cta_list[0]
        return cta_template.format(**kwargs)

    def _gen_id(self) -> str:
        """生成简短ID"""
        import time
        return str(int(time.time()))[-6:]

    def generate_batch(self, topics: List[str], **kwargs) -> List[Script]:
        """批量生成脚本"""
        scripts = []
        for topic in topics:
            script = self.generate(topic, **kwargs)
            scripts.append(script)
        return scripts


# ============ 便捷函数 ============

def gen_script(
    topic: str,
    template: str = "tool_review",
    hook: str = "conflict",
    duration: float = 90.0,
    **kwargs
) -> Dict:
    """
    生成单个脚本的便捷函数

    Args:
        topic: 话题主题
        template: 模板类型 (tool_review/money_case/workflow/hot_analysis)
        hook: 钩子类型 (conflict/numeric/suspense/question/comparison/emotion)
        duration: 目标时长
        **kwargs: 额外参数 (old_tool, ai_tool, amount, days等)

    Returns:
        脚本JSON字典
    """
    config = ScriptConfig(
        template=ScriptTemplate(template),
        hook_type=HookType(hook),
        target_duration=duration
    )

    generator = YunfanScriptGenerator(config)
    script = generator.generate(topic, **kwargs)

    return script.to_dict()


def gen_batch(
    topics: List[str],
    template: str = "tool_review",
    hook: str = "conflict",
    **kwargs
) -> List[Dict]:
    """批量生成脚本"""
    config = ScriptConfig(
        template=ScriptTemplate(template),
        hook_type=HookType(hook)
    )

    generator = YunfanScriptGenerator(config)
    scripts = generator.generate_batch(topics, **kwargs)

    return [s.to_dict() for s in scripts]


# ============ CLI 入口 ============

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python yunfan_script_gen.py <topic> [options]")
        print("Options:")
        print("  --template <type>  : tool_review/money_case/workflow/hot_analysis")
        print("  --hook <type>      : conflict/numeric/suspense/question/comparison/emotion")
        print("  --duration <sec>   : target duration in seconds")
        print("  --ai-tool <name>   : AI tool name")
        print("  --old-tool <name>  : old tool name")
        print("  --amount <money>   : money amount for case")
        sys.exit(1)

    topic = sys.argv[1]

    # 解析参数
    template = "tool_review"
    hook = "conflict"
    duration = 90.0
    ai_tool = "AI工具"
    old_tool = "传统工具"
    amount = "5000"

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--template":
            template = sys.argv[i+1]
        elif sys.argv[i] == "--hook":
            hook = sys.argv[i+1]
        elif sys.argv[i] == "--duration":
            duration = float(sys.argv[i+1])
        elif sys.argv[i] == "--ai-tool":
            ai_tool = sys.argv[i+1]
        elif sys.argv[i] == "--old-tool":
            old_tool = sys.argv[i+1]
        elif sys.argv[i] == "--amount":
            amount = sys.argv[i+1]
        i += 2

    # 生成脚本
    result = gen_script(
        topic,
        template=template,
        hook=hook,
        duration=duration,
        ai_tool=ai_tool,
        old_tool=old_tool,
        amount=amount
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    # 写入文件确保中文正确显示
    with open("last_script.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
