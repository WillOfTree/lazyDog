#! coding=utf-8
import pymysql
import time


class LionDb(object):
    LOG_PATH = "./log_info.txt"

    def __init__(self, item):
        self.movie_item = item  # 保存数据
        # 打开数据库连接
        self.db = pymysql.connect(
            "localhost",
            "root",
            "humingfei212697~",
            "codelion",
        )

        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()

    # @classmethon
    def judgeSave(self):
        '''
            验证指定name的电影是否存在，存在验证是否需要跟新，不存在返回True

            name：电影名称
            date: 电影上次更新日期更新的日期
            return : True,False,集数
        '''
        name = self.movie_item['name']

        select_save = "SELECT id,time,state FROM movie_info WHERE `name` = %s" % (
            repr(name))  # 查询语句，电影名称是否存在

        self.cursor.execute(select_save)
        data = self.cursor.fetchone()  # 获取是否存在

        if data:
            ''' 电影存在，真'''
            if data[2] is not "end":  # data是一个数组
                '''未完结'''
                movie_time = self.movie_item['time']  # 获取当前电影跟新日期
                # ValueError: time data '1514995200' does not match format '%Y-%m-%d'
                if movie_time > int(data[1]):
                    '''返回当前集数'''
                    print(data[2])
                    return str(data[2])

                return int(1)
            else:
                '''电影完结，退出'''
                return False

        else:
            '''当前电影不存在，返回True'''
            return True

    def insert_data(self):
        '''
            添加数据
            return : image_name
        '''
        name = self.movie_item['name']
        s_type = self.movie_item['type']
        time = self.movie_item['time']
        state = self.movie_item['state']
        image = self.movie_item['image_name']

        # 添加电影信息
        insert_movie = "INSERT INTO movie_info(`name`,`type`,`time`,`hot`,`hidden`,`state`,`image`) VALUES(%s,%s,%s,%s,%s,%s,%s)"

        try:
            a = self.cursor.execute(
                insert_movie, (name, s_type, time, '0', '1', state, image))  # 执行插入语句
            if a == 1:
                print("INsert OK")
            else:
                print("Error")

        except BaseException as err:
            with open(self.LOG_PATH, "a+") as f:
                f.write("insert movie_info FALSE \r\nURL:%s\r\nERR:%s----------------------\r\n" %
                        (self.movie_item['url'], err))
            self.db.rollback()

        movie_id = self.cursor.lastrowid  # 插入的id
        b = self.db.commit()  # 提交

        self.__instert_links(self.movie_item['baidu_links'], movie_id)
        self.__instert_links(self.movie_item['magnetic'], movie_id)  # 磁力链接插入

    def __instert_links(self, item, movie_id):
        '''
            向links表中添加数据,向log_info中添加日志
            movie_id:电影详情id
            item:要添加的数据
        '''

        if item:
            save_link = []  # 保存链接数据
            for b_link in item:
                # describe 第一集，第二集等
                save_link.append(
                    (b_link[1], self.movie_item['type'], movie_id, b_link[0]))

            insert_links = "INSERT INTO links(`link`,`type`,`movie_id`,`describe`) VALUES(%s,%s,%s,%s)"
            try:
                self.cursor.executemany(insert_links, save_link)  # 同时提交多条
            except BaseException as err:
                self.db.rollback()  # 滚回

                with open(self.LOG_PATH, "a+", encoding="utf-8") as f:
                    f.write("Warning:插入失败\r\nURL:%s\r\nERROR:%s---------------\r\n" %
                            (self.movie_item['url'], err))
                return False

            self.db.commit()  # 提交

            '''日志，方便以后检查'''
            with open(self.LOG_PATH, "a+", encoding="utf-8") as f:
                leng = len(save_link)  # 列表长度

                f.write("success write into table:links\r\nNum:%d\n\rID:%s\r\nURl:%s---------------\r\n" % (
                    leng, self.cursor.lastrowid, self.movie_item['url']))

            return True
        else:

            with open(self.LOG_PATH, "a+", encoding="utf-8") as f:
                f.write("Warning:空\r\nURL:%s\r\n---------\r\n" %
                        (self.movie_item['url']))
            return False

    def updata_data(self, movie_num):
        '''更新方法'''
        num = int(movie_num)
        b_links = self.movie_item['baidu_links']
        m_links = self.movie_item['magnetic']
        for i in range(num):
            del b_links[i]
            del m_links[i]
        with open(self.LOG_PATH, "a+", encoding="utf-8") as f:
            f.write("updata_info:-----------\r\n%s\r\n----------\r\%s\r\n" %
                    (b_links, m_links))
        self.__instert_links(b_links, movie_id)  # 百度连接插入
        self.__instert_links(m_links, movie_id)  # 磁力链接插入

    def close(self):
        self.db.close()
