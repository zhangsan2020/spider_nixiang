import json
import os
import random
import time

import execjs
import requests
from .useragent import useragent_pool
from .redis_toubiao import RedisCli
from .mongo_store_toubiao import MongoStore
class CTB():
    def __init__(self):
        # http://ctbpsp.com/#/
        self.redis_cli = RedisCli()
        self.mongo_cli = MongoStore()

    def get_des_data(self, message):

        with open('D:/live/all_study_new/spider/des_test.js', 'r') as f:
            reader = f.read()
        loader = execjs.compile(reader)
        des_data = loader.call('decryptByDES', message)
        return des_data

    def downloader(self, url):
        headers = {
            "User-Agent": random.choice(useragent_pool),
            "Host": "custominfo.cebpubservice.com"
        }
        res = requests.get(url, headers=headers, verify=False)
        if res.status_code == 200:
            return res.text.strip().replace('"',"")
        else:
            print('数据出错')

    def parse_data(self, data):
        json_str = self.get_des_data(data)
        json_data = json.loads(json_str)
        # print(json_data)
        # print(type(json_data))
        data_list = json_data['data']['dataList']
        for data in data_list:
            item = {}
            item['id'] = data['bulletinID']
            item['noticeName'] = data['noticeName']
            item['noticeMedia'] = data['noticeMedia']
            item['tradePlat'] = data['tradePlat']
            item['regionCode'] = data['regionCode']
            item['date'] = data['noticeSendTime']
            item['noticeUrl'] = data['noticeUrl']
            print(item)
            yield item

    def run(self):
        flag = 1
        for i in range(1,10):
            url = "https://custominfo.cebpubservice.com/cutominfoapi/recommand/type/5/pagesize/10/currentpage/{}".format(i)
            print('当前是第 {} 页'.format(i))
            data = self.downloader(url)
            time.sleep(2)
            print(data)
            datas = self.parse_data(data)
            for item in datas:
                to_md5 = item['id'] + item['date'] + item['noticeUrl']
                status = self.redis_cli.set_item('toubiao_data',to_md5)
                print('当前状态是: {}'.format(status))
                if status == 1:
                    self.mongo_cli.insert(item)
                elif status == 0:

                    print('当前数据已经抓取过了, 不在抓取')
                    flag = 0
                    break
                else:
                    print('当前插入数据状态异常!!!')
            if flag == 0:
                print('停止当前进程!!')
                break


# if __name__ == '__main__':
#     ctb = CTB()
#     ctb.run()
