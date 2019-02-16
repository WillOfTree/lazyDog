# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .lion_db_class import LionDb


class LionPipeline(object):

    def process_item(self, item, spider):

        # self.movie_item = item  # 保存到类属性
        LionDB = LionDb(item)

        state = LionDB.judgeSave()  # 判断电影状态

        if isinstance(state, bool):  # 真，电影不存在，假，电影不需要更新
            if state:
                '''True 电影不存在'''
                LionDB.insert_data()

        if isinstance(state, str):
            '''跟新指定集数'''
            LionDB.updata_data(state)

        # 关闭数据库连接
        LionDB.close()

        return item
