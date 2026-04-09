#!/usr/bin/env python3
"""
微信公众号文章获取脚本
使用 DrissionPage 控制 Chrome 浏览器获取文章内容
"""

import sys
import os

def fetch_article(url, headless=False):
    """
    获取微信公众号文章内容

    Args:
        url: 微信公众号文章链接
        headless: 是否使用无头模式（默认 False，显示浏览器窗口）

    Returns:
        dict: 包含 title, url, content 的字典
    """
    try:
        from DrissionPage import ChromiumPage, ChromiumOptions
    except ImportError:
        print("错误: DrissionPage 未安装", file=sys.stderr)
        print("请运行: pip install DrissionPage", file=sys.stderr)
        sys.exit(1)

    # 配置选项
    options = ChromiumOptions()
    if headless:
        options.headless()

    try:
        # 加上时间戳参数绕过微信 CDN 缓存
        import time as _time
        cache_buster = f"_t={int(_time.time() * 1000)}"
        if "?" in url:
            fetch_url = f"{url}&{cache_buster}"
        else:
            fetch_url = f"{url}?{cache_buster}"

        print(f"正在启动浏览器获取文章: {fetch_url}", file=sys.stderr)

        # 创建页面对象
        page = ChromiumPage(options)

        # 访问页面（带时间戳绕过缓存）
        page.get(fetch_url)

        # 等待页面加载
        page.wait(3)

        # 获取标题
        title = page.title
        print(f"文章标题: {title}", file=sys.stderr)

        # 等待文章内容加载
        try:
            page.wait.ele_displayed('#js_content', timeout=10)
        except:
            print("警告: 未找到文章正文元素，尝试获取页面全部文本", file=sys.stderr)

        # 获取内容
        try:
            content_elem = page.ele('#js_content')
            text_content = content_elem.text
        except:
            text_content = page.ele('body').text

        print(f"获取内容长度: {len(text_content)} 字符", file=sys.stderr)

        # 截图
        try:
            page.get_screenshot(path='article_screenshot_weixin.png', full_page=True)
            print("截图已保存: article_screenshot_weixin.png", file=sys.stderr)
        except Exception as e:
            print(f"截图失败: {e}", file=sys.stderr)

        # 格式化输出
        result_text = f"\n{'='*60}\n"
        result_text += f"TITLE: {title}\n"
        result_text += f"{'='*60}\n"
        result_text += (text_content[:5000] if text_content else '未找到文章内容') + "\n"
        if len(text_content) > 5000:
            result_text += "\n... (内容已截断，完整内容请查看文件)\n"
        result_text += f"{'='*60}\n"

        # 保存到文件
        output_file = 'article_content_weixin.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result_text)
        print(f"内容已保存: {output_file}", file=sys.stderr)

        # 打印结果
        print(result_text)

        # 等待几秒后关闭
        if not headless:
            page.wait(2)

        return {
            'title': title,
            'url': url,
            'content': text_content,
            'output_file': output_file
        }

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return {'error': str(e), 'url': url}
    finally:
        try:
            page.quit()
        except:
            pass


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python fetch_weixin.py <微信公众号文章URL>")
        print("示例: python fetch_weixin.py 'https://mp.weixin.qq.com/s/xxxxx'")
        sys.exit(1)

    url = sys.argv[1]

    if not url.startswith('https://mp.weixin.qq.com/'):
        print(f"警告: URL 看起来不是微信公众号文章链接: {url}")

    result = fetch_article(url)

    if 'error' in result:
        print(f"获取失败: {result['error']}")
        sys.exit(1)
    else:
        print(f"\n✅ 获取成功!")
        print(f"标题: {result['title']}")
        print(f"内容长度: {len(result['content'])} 字符")
        print(f"保存文件: {result['output_file']}")


if __name__ == '__main__':
    main()