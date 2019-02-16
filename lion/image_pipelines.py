# -*- coding: utf-8 -*-

import time
import scrapy
import re
import os

from scrapy.utils.project import get_project_settings  # 导入setting文件
from scrapy.pipelines.images import ImagesPipeline


class ImgPipeline(ImagesPipeline):
    IMAGE_SOURCE = get_project_settings().get("IMAGES_STORE")

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     print("xxxxxxxxxxxxxxxxxxxxxxxxx")

    def get_media_requests(self, item, info):  # 发送请求
        # item就是items.py中定义的变量集合
        # 这里可以修改申请下载的文件
        yield scrapy.Request(item['image'])

    def item_completed(self, result, item, info):  # 处理图片
        image_path = [x['path'] for ok, x in result if ok]

        # 重保存位置
        os.rename(self.IMAGE_SOURCE + '/' +
                  image_path[0], self.IMAGE_SOURCE + '/' + item['image_name'])

        return item
