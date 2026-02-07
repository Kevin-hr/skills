# 雲帆AI脚本生成器使用示例

## 1. 单个脚本生成

```bash
cd scripts

# 工具测评模板
python yunfan_script_gen.py "AI写作工具" --template tool_review --ai-tool "ChatGPT" --old-tool "手工写作"

# 变现案例模板
python yunfan_script_gen.py "AI副业赚钱" --template money_case --amount "8000" --days "30"

# 工作流模板
python yunfan_script_gen.py "AI批量作图" --template workflow --ratio "10"

# 热点解读模板
python yunfan_script_gen.py "DeepSeek热点" --template hot_analysis --hook suspense
```

## 2. 批量生成

```python
from yunfan_script_gen import gen_batch

topics = [
    "AI视频生成",
    "AI写作工具",
    "AI抠图软件",
    "AI语音合成"
]

scripts = gen_batch(
    topics,
    template="tool_review",
    hook="conflict"
)

for s in scripts:
    print(f"脚本ID: {s['script_id']}, 时长: {s['total_duration']}秒")
```

## 3. API调用示例

```python
import requests
import json

# 假设有API服务
response = requests.post(
    "http://localhost:8000/gen_script",
    json={
        "topic": "AI PPT工具",
        "template": "tool_review",
        "hook": "numeric",
        "ai_tool": "Gamma",
        "old_tool": "手工做PPT"
    }
)

script = response.json()
print(json.dumps(script, indent=2, ensure_ascii=False))
```

## 4. 输出格式示例

```json
{
  "script_id": "sr_123456",
  "template_type": "tool_review",
  "topic": "AI写作工具",
  "hook_type": "conflict",
  "total_duration": 90.0,
  "scene_count": 5,
  "scenes": [
    {
      "scene_id": 1,
      "duration": 3.0,
      "content": "大字标题：别再用传统工具了！这个AI工具免费还更强",
      "narration": "开场白：别再用传统工具了",
      "visual_style": "冲击文字"
    }
  ],
  "core_principles": ["有用性", "开头承诺", "AI对比"],
  "cta": "想要工具包的，评论区扣1"
}
```

## 5. 模板与钩子组合

| 模板类型 | 推荐钩子 | 适用场景 |
|---------|---------|---------|
| tool_review | conflict/comparison | 工具横评、替代方案 |
| money_case | numeric/emotion | 成功案例、收入展示 |
| workflow | numeric/comparison | 效率提升、流程优化 |
| hot_analysis | suspense/question | 热点解读、趋势分析 |
