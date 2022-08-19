import pika
import json

class MQ():

    credentials = pika.PlainCredentials('guest', 'guest')  # mq用户名和密码

    def __init__(self):
        # 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='127.0.0.1', port=5672, virtual_host='/', credentials=self.credentials))
        self.channel = self.connection.channel()
        # 声明消息队列，消息将在这个队列传递，如不存在，则创建
        self.channel.queue_declare(queue = 'food_detail_urls')

    def insert(self,detail_url):
        # for i in range(10):
        #     message=json.dumps({'OrderId':"1000%s"%i})
        # 向队列插入数值 routing_key是队列名
        self.channel.basic_publish(exchange = '',routing_key = 'food_detail_urls',body = detail_url)


    def recive(self,):
        self.channel.queue_declare(queue='food_detail_urls', durable=False)

        # 定义一个回调函数来处理消息队列中的消息，这里是打印出来
        def callback(ch, method, properties, body):
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(body.decode())

        # 告诉rabbitmq，用callback来接收消息
        self.channel.basic_consume('food_detail_urls', callback)
        # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
        self.channel.start_consuming()