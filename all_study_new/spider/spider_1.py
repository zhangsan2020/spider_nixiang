import random
import time

import redis
import requests
import aiohttp
import asyncio
import requests
from requests.adapters import HTTPAdapter
from .useragent import useragent_pool
from lxml import etree
from .redis_ import RedisCli
from ..rabbit_mq.mq import MQ


class FoodUrls():
    '''
    当前类用于获取所有的链接, 经过比对去重之后将数据放入 rabbitmq里头做详情页数据的抓取
    '''
    # url_first = 'https://home.meishichina.com/recipe-type.html'
    recai_url = 'https://home.meishichina.com/recipe/recai/'
    redis_cli = RedisCli()
    redis_urls = 'detail_urls'
    mq = MQ()




    def downlader(self, url):

        # async with aiohttp.ClientSession() as session:
        #     async with session.get(url) as res:
        #         if res.status == 200:
        #             content = await res.text(encoding='utf-8')
        #             return content
        #         else:
        #             return None
        useragent = random.choice(useragent_pool)
        headers = {
            'user-agent': useragent
        }
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))

        res = s.get(url, headers=headers, timeout=5, verify=False)
        time.sleep(random.random())
        res.encoding = 'utf-8'
        # print(res.text)

        if res.status_code == 200:
            return res.text
        else:
            print('错误的返回是:  ',res.text)
            print('请求数据为空,链接地址为: ',url)

    def parser(self, content):
        '''
        解析出所有的链接与item数据, 如果链接已经存在不在抓取返回 0, 否则继续抓取
        当前先获取格式统一的模块结构进行抓取
        :param content:
        :return: item与url
        '''
        pass
        # page_items = {}
        item = {}
        parser_content = etree.HTML(content)
        divs = parser_content.xpath('//div[@class="detail"]')
        for div in divs:
            page_items = {}
            item['name'] = div.xpath('./h2/a/text()')[0]
            item['author'] = div.xpath('./p[@class="subline"]/a/text()')[0]
            item['food_source'] = div.xpath('./p[@class="subcontent"]/text()')[0]
            item['detail_url'] = div.xpath('./h2/a/@href')[0]
            page_items[item['detail_url']] = item
            # print(item)
            yield page_items

    def redis_duplicate(self, key, item):
        '''
        使用redis集合进行md5 url比对, 如果存在就不再抓取当前url, 不存在放入rabbitmq进行保存
        :param item:
        :return: 0/1 为0 代表集合中存在已经抓取过, 否则存入集合继续抓取
        '''

        url = self.redis_cli.set_item(key, item)
        print('当前去重的结果是: ', url)
        if url:
            self.mq.insert(url)

    # def next_page_exists(self):
    #     useragent = random.choice(useragent_pool)
    #     headers = {
    #         'user-agent': useragent
    #     }
    #     url_type_0 = 'https://home.meishichina.com/recipe-type.html'
    #     url_type_1 = {}
    #     data = self.downlader(url_type_0)
    #     html = etree.HTML(data)
    #     divs = html.xpath('//div[@class="category_sub clear"]')
    #     all_type_urls = {}
    #     for div in divs:
    #         name_0 = div.xpath('./h3/text()')[0]
    #         lis = div.xpath('.//li')
    #         items = {}
    #         print(lis)
    #         for li in lis:
    #             # print(li.text())
    #             name_1 = li.xpath('./a/text()')[0]
    #             print(name_1)
    #             name_1_url = li.xpath('./a/@href')[0]
    #             print(name_1_url)
    #             # print(name_1,name_1_url)
    #         # print(name_0, name_1, name_1_url)
    #             items[name_1] = name_1_url
    #         all_type_urls[name_0] = items
    #     # print('这是要看的数据: ', all_type_urls)
    #     return all_type_urls
    def run(self):
        '''
        负责当前爬虫的调度
        :return:
        '''

        for i in range(1,2001):
            print('当前是第 {} 页'.format(i)*10)
            url = 'https://home.meishichina.com/recipe/recai/page/{}/'.format(i)
            content = self.downlader(url)
            # print(content)
            if content:
                page_items = self.parser(content)
                # print(page_items)
                # page_items_ = {}
                for page_item in page_items:
                    # print(page_item)
                    self.redis_duplicate(self.redis_urls, page_item)

    def mongo_store(self, item):
        '''
        存储当前拿到的每一条数据
        :param item:
        :return:
        '''
        pass

    def main(self):

        '''
        开启多协程抓取数据(3个协程)
        :return:
        '''
        pass
        self.run()


if __name__ == '__main__':
    '''
    爬虫测试入口, 用于测试当前爬虫程序是否正常
    '''
    food = FoodUrls()
    food.main()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(food.main())
