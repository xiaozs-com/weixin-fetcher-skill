# 微信公众号文章获取 Skill

> 获取微信公众号文章正文内容，用于 AI Agent 工作流

## 功能

- 自动获取微信公众号文章（mp.weixin.qq.com）的标题和正文
- 自动绕过微信 CDN 缓存，获取最新内容
- 支持截图保存
- 基于 DrissionPage + Chrome 浏览器

## 安装

### 1. 安装依赖

```bash
pip install DrissionPage
```

### 2. 克隆本仓库

将仓库克隆到你的 OpenClaw skills 目录：

```bash
git clone https://github.com/xiaozs-com/weixin-fetcher-skill.git <你的skills目录>/weixin-fetcher-skill
```

或者直接下载 SKILL.md 和 scripts/fetch_weixin.py 到对应位置。

## 使用方法

### 命令行

```bash
python scripts/fetch_weixin.py "https://mp.weixin.qq.com/s/xxxxx"
```

### Python 代码

```python
from scripts.fetch_weixin import fetch_article

result = fetch_article("https://mp.weixin.qq.com/s/xxxxx")
print(result['title'])
print(result['content'][:500])
```

## 输出文件

| 文件 | 说明 |
|------|------|
| article_content_weixin.txt | 文章标题和正文 |
| article_screenshot_weixin.png | 页面截图 |

## 系统要求

- Python 3.7+
- Chrome 浏览器（系统已安装）
- DrissionPage

## License

MIT