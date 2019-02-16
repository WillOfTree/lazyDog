# -*- coding: utf-8 -*-
import scrapy
import time
import re
import os

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from lion.items import LionItem


class YyspiderSpider(CrawlSpider):
    name = 'yySpider'
    allowed_domains = ['www.yyetss.com']
    # 起始页
    start_urls = ['http://www.yyetss.com/list-lishi-all-1.html']

    link_detail = LinkExtractor(allow=("detail-\d+\.html"))  # 匹配页面中的内容
    link_url = LinkExtractor(allow=("\/list\-lishi\-all\-\d+\.html"))  # 匹配页码

    rules = [
        Rule(link_url, follow=True),  # 获取页面中页码信息
        Rule(link_detail, callback="parse_content", follow=False)  # 每一页中的数据进行处理
    ]

    # CrawlSpider不能重写parse方法
    # def parse(self, response):
    # 处理页面中的信息
    def parse_content(self, request):
        item = LionItem()
        # 名字
        name = request.xpath(
            "//div[@class='row']/div[@class='col-xs-8 col-sm-4 col-md-4']/p[1]/text()").extract()[0]
        tem_name = name.split("\xa0")
        if len(tem_name) == 2:
            item['name'] = tem_name[0]
            tem_name[1] = tem_name[1].lstrip('(')
            item['type'] = tem_name[1].rstrip(')')
        else:
            item['name'] = tem_name[0].replace("\xa0", "")
            item['type'] = 'TV'  # 将不可识别的字符替换

        # 时间
        data = request.xpath(
            "//div[@class='row']/div[@class='col-xs-8 col-sm-4 col-md-4']/p[4]/text()").extract()[0]
        item['time'] = int(time.mktime(time.strptime(data, "%Y-%m-%d")))

        # 百度链接
        b_links = request.xpath("//ul[@class='pan']/li/a")
        baidulinks = []
        for b_link in b_links:
            bl = b_link.xpath("./@href").extract()[0]  # 地址
            bn = b_link.xpath("./text()").extract()[0]  # 标题
            baidulinks.append([bn, bl])

        item['baidu_links'] = baidulinks
        # 磁力链接
        m_links = request.xpath("//div[@class='tab_set_info'][2]/ul/li/a")
        magnetics = []
        for n in m_links:
            ml = n.xpath("./@href").extract()[0]  # 地址
            mn = n.xpath("./text()").extract()[0]  # 标题
            magnetics.append([mn, ml])

        '''获取照片位置'''
        image_path = request.xpath(
            "//div[@class='row']/div[@class='col-xs-3 col-sm-3 col-md-3']/img/@src").extract()[0]

        '''获取当前集数与结果'''
        stateData = request.xpath(
            "//span[@class='label label-success']/text()").extract()[0]

        pattern_num = re.compile(r"至第(\d+)集")
        state = pattern_num.search(stateData)

        if state:
            item['state'] = state.group(1)
        else:
            item['state'] = "end"

        # 确定电影名称
        a = image_path.split('!')
        time_name = str(round(time.time() * 1000))

        if len(a) == 2:
            a_path = os.path.splitext(a[0])
            a_res = time_name + a_path[1]
        else:
            a_res = time_name + '.jpg'

        item['magnetic'] = magnetics

        item['url'] = request.url
        item['image'] = image_path
        item['image_name'] = a_res

        yield item
