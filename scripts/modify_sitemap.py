# coding=utf-8
import xml.etree.ElementTree as ET
import os
from datetime import date


def add_custom_loc_to_sitemap(sitemap_path, custom_urls):
    # 注册命名空间
    ET.register_namespace('', "http://www.sitemaps.org/schemas/sitemap/0.9")

    # 解析现有的 sitemap.xml 文件
    tree = ET.parse(sitemap_path)
    root = tree.getroot()

    # 获取当前日期
    today = date.today().isoformat()

    # 为每个自定义 URL 创建新的 url 元素
    for url in custom_urls:
        url_element = ET.SubElement(root, 'url')
        loc = ET.SubElement(url_element, 'loc')
        loc.text = url

        # 添加 changefreq 元素
        changefreq = ET.SubElement(url_element, 'changefreq')
        changefreq.text = 'daily'

        # 添加 lastmod 元素
        lastmod = ET.SubElement(url_element, 'lastmod')
        lastmod.text = today

    # 将修改后的 XML 写回文件
    tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)

    # 读取文件内容
    with open(sitemap_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 替换 XML 声明行，确保它符合期望的格式
    content = content.replace('<?xml version="1.0" encoding="utf-8"?>',
                              '<?xml version="1.0" encoding="UTF-8"?>')

    # 写回修改后的内容
    with open(sitemap_path, 'w', encoding='utf-8') as file:
        file.write(content)


# 使用示例
if __name__ == "__main__":
    sitemap_path = 'docs/site/sitemap.xml'  # MkDocs 生成的 sitemap.xml 的路径
    custom_urls = [
        'https://django-ninja.cn/online-tools/py312run/console.html',
        'https://django-ninja.cn/online-tools/996-Salary-Calculator/',
        'https://django-ninja.cn/online-tools/python-tutor/'
    ]

    if os.path.exists(sitemap_path):
        add_custom_loc_to_sitemap(sitemap_path, custom_urls)
        print("Sitemap 已成功更新!")
    else:
        print("Sitemap 文件不存在!")
