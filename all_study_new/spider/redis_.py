import redis
import hashlib
class RedisCli():

    def __init__(self):

        # self.redis_cli = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        self.redis_cli = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def set_item(self,name,item):
        '''
        放入集合进行去重
        :param name:
        :param item:
        :return:
        '''
        md5_url = self.md5_(item)
        flag = self.redis_cli.sadd(name,md5_url)
        if flag == 1:
            print('插入集合成功!!')
            return [v['detail_url'] for v in item.values()][0]
        elif flag == 0:
            print('链接地址已经请求过不在放入mq再次发起请求!!')
            return 0
        else:
            print('插入集合存在其它问题')

    def md5_(self,item):

        for item_key in item:
            print('当前键为: ',item_key)
            m = hashlib.md5()
            m.update(item_key.encode())
            md5_url = m.hexdigest()
            print(item,md5_url)
            return md5_url
