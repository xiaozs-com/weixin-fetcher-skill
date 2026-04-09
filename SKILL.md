---
name: weixin-fetcher
description: 获取微信公众号文章内容。当用户提供微信公众号文章链接（mp.weixin.qq.com）时使用此技能提取文章正文内容。触发场景：用户发送微信公众号文章链接、要求获取/提取/查看公众号文章内容、提到"微信公众号"、"微信文章"、"公众号文章"等关键词。
---

# 微信公众号文章获取 Skill

使用 DrissionPage 控制 Chrome 浏览器获取微信公众号文章内容。

## 何时使用

- 用户发送微信公众号文章链接（格式：https://mp.weixin.qq.com/s/...）
- 用户要求获取/提取/查看微信公众号文章内容
- 用户提到"微信公众号"、"微信文章"、"公众号文章"

## 使用方法

### 1. 直接执行脚本

`ash
python skills/weixin-fetcher/scripts/fetch_weixin.py "<文章URL>"
`

### 2. Python 代码调用

`python
from skills.weixin_fetcher.scripts.fetch_weixin import fetch_article

result = fetch_article("https://mp.weixin.qq.com/s/...")
print(result['title'])
print(result['content'])
`

## 依赖安装

首次使用前需要安装依赖：

`ash
pip install DrissionPage
`

## 工作原理

1. **启动 Chrome 浏览器** - 使用 DrissionPage 启动系统 Chrome（有头模式）
2. **绕过缓存** - 自动在 URL 末尾加上时间戳参数，避免微信 CDN 返回缓存内容
3. **访问文章页面** - 浏览器自动打开微信公众号文章
4. **等待内容加载** - 等待 #js_content 元素出现
5. **提取正文** - 提取文章标题和正文内容
6. **保存结果** - 保存到文件并截图

## 输出文件

- rticle_content_weixin.txt - 文章标题和正文
- rticle_screenshot_weixin.png - 页面截图

## 注意事项

- 需要系统已安装 Chrome 浏览器
- 首次运行可能需要下载匹配的 ChromeDriver

## 示例

`ash
# 获取单篇文章
python skills/weixin-fetcher/scripts/fetch_weixin.py "https://mp.weixin.qq.com/s/EVdnYEzlrT3BZZUmlbxHQQ"
`

## 技术细节

- **框架**: DrissionPage (基于 Selenium/ChromeDriver)
- **浏览器**: Chrome (系统已安装的版本)
- **选择器**: #js_content (微信公众号文章正文容器)
- **编码**: UTF-8

## 作者

- 创建时间: 2026-03-28
- 版本: 1.0