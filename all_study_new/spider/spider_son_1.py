import random
import time

import aiohttp
import pymongo
from lxml import etree

import pika
import requests
from requests.adapters import HTTPAdapter
from .useragent import useragent_pool
from .mongo_store import MongoStore
import asyncio
from queue import Queue
import _thread

class FoodSon():
    credentials = pika.PlainCredentials('guest', 'guest')  # mq用户名和密码
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='127.0.0.1', port=5672, virtual_host='/', credentials=self.credentials))
        self.channel = self.connection.channel()
        # 声明消息队列，消息将在这个队列传递，如不存在，则创建
        self.channel.queue_declare(queue = 'food_detail_urls')
        self.mongocli = MongoStore()
        self.q = Queue()
        self.loop = asyncio.get_event_loop()

    # def get_msg(self):
    #
    #     data = self.mq.recive()
    #     print('当前数据为: ', data)

    def downlader(self, url):

        useragent = random.choice(useragent_pool)
        # headers = {
        #     'user-agent': useragent
        # }
        # async with aiohttp.ClientSession() as session:
        #     async with session.get(url) as res:
        #         if res.status == 200:
        #             content = await res.text(encoding='utf-8')
        #             return content
        #         else:
        #             return None
        # useragent = random.choice(useragent_pool)
        headers = {
            'user-agent': useragent
        }
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))

        res = s.get(url, headers=headers, timeout=5)
        time.sleep(random.random())
        res.encoding = 'utf-8'
        # print(res.text)

        if res.status_code == 200:
            return res.text
        else:
            print('错误的返回是:  ',res.text)
            print('请求数据为空,链接地址为: ',url)

    def parser(self,content):
        item = {}
        html = etree.HTML(content)
        title = html.xpath('//a[@id="recipe_title"]/text()')[0]
        author = html.xpath('//span[@id="recipe_username"]/text()')[0]
        img_url = html.xpath('//a[@class="J_photo"]/img/@src')[0]
        # print(title,author,img_url)
        item['title'] = title
        item['author'] = author
        item['img_url'] = img_url
        print(item)
        return item
    def mongo_store(self,item):
        pass
        res = self.mongocli.insert(item)
        print(res)

    def aio_run(self,url):
        print('当前的url是: {}'.format(url))
        html = self.downlader(url)
        # print(html)
        item = self.parser(html)
        # time.sleep(random.random())
        self.mongo_store(item)
    # def run_task(self):
    #     aio_tasks = []
    #     while not self.q.empty():
    #         url = self.q.get()
    #         aio_tasks.append(self.aio_run(url))
    #         if len(aio_tasks) == 3:
    #             self.loop.run_until_complete(asyncio.wait(aio_tasks))
    #             aio_tasks.clear()

    # 定义一个回调函数来处理消息队列中的消息，这里是打印出来
    def callback(self,ch, method, properties, body):

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(body)
        url = body.decode()
        # time.sleep(3)
        html = self.downlader(url)
        # # print(html)
        item = self.parser(html)
        # # time.sleep(random.random())
        self.mongo_store(item)


    def recive(self):
        self.channel.queue_declare(queue='food_detail_urls', durable=False)
        # 告诉rabbitmq，用callback来接收消息
        self.channel.basic_consume('food_detail_urls', self.callback)
        # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
        self.channel.start_consuming()
