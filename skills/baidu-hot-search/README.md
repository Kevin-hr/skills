# baidu-hot-search

> 百度热搜获取工具 - 支持网页解析和API双通道

## 功能特性

- 获取百度热搜榜（多分类：民生、财经、体育、娱乐、科技等）
- 批量获取TOP N热点关键词
- 支持JSON格式输出，便于程序处理
- 兼容百度NLP API（如有授权）

## 使用方式

### 基础命令

```bash
# 获取热搜榜TOP10
python scripts/baidu_hot_search.py

# 获取财经榜TOP20
python scripts/baidu_hot_search.py --category finance --limit 20

# JSON格式输出
python scripts/baidu_hot_search.py --format json --output hot.json

# 获取科技榜
python scripts/baidu_hot_search.py --category tech
```

### 可用分类

| 参数 | 名称 | 说明 |
|:---|:---|:---|
| hot | 热搜榜 | 全站热搜 |
| domestic | 国内榜 | 国内热点 |
| abroad | 国际榜 | 国际热点 |
| finance | 财经榜 | 财经资讯 |
| sports | 体育榜 | 体育新闻 |
| entertainment | 娱乐榜 | 娱乐八卦 |
| education | 教育榜 | 教育资讯 |
| tech | 科技榜 | 科技动态 |
| game | 游戏榜 | 游戏资讯 |
| car | 汽车榜 | 汽车资讯 |
| estate | 房产榜 | 房产资讯 |
| travel | 旅游榜 | 旅游资讯 |

## 输出示例

```
【热搜榜】- 2024-01-15 14:30:25
------------------------------------------------------------
 1. 特斯拉发布新车型 (热度: 1256800)
    🔗 https://baidu.com/s?word=特斯拉发布新车型
 2. 2024年春运火车票开售 (热度: 980500)
    🔗 https://baidu.com/s?word=2024年春运火车票开售
...
```

## 依赖安装

```bash
pip install requests beautifulsoup4 lxml
```

## 集成到项目

```python
from baidu_hot_search import BaiduHotSearch

hot = BaiduHotSearch()
result = hot.get_hot_list("tech", 20)

if result["success"]:
    for item in result["data"]:
        print(f"{item['rank']}. {item['keyword']}")
```

## API说明

### `BaiduHotSearch.get_hot_list(category, limit)`

获取指定分类的热搜榜单。

**参数:**
- `category` (str): 分类名称，如 "hot", "finance", "tech"
- `limit` (int): 返回数量限制

**返回:**
```python
{
    "success": True,
    "category": "科技榜",
    "fetch_time": "2024-01-15 14:30:25",
    "total": 20,
    "data": [
        {
            "rank": 1,
            "keyword": "关键词",
            "heat": 123456,
            "url": "https://...",
            "source": "baidu-html"
        }
    ]
}
```

## 注意事项

1. **网页解析方案**：默认使用网页解析，无需API授权
2. **官方API状态**：百度NLP热点API处于邀测状态，需官方授权才能使用
3. **频率限制**：请勿过于频繁请求，建议间隔30秒以上
4. **数据来源**：解析结果仅供参考，请以百度官方数据为准

## License

MIT
