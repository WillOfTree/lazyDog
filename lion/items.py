# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LionItem(scrapy.Item):
    # define the fields for your item here like:
    # 保存电影名称
    name = scrapy.Field()
    # 百度云地址
    baidu_links = scrapy.Field()
    # 类型
    type = scrapy.Field()
    # 磁力链接地址
    magnetic = scrapy.Field()
    # 时间
    time = scrapy.Field()
    # 状态
    state = scrapy.Field()
    # url
    url = scrapy.Field()
    # 照片
    image = scrapy.Field()
    # 数据库保存的照片名称
    image_name = scrapy.Field()
