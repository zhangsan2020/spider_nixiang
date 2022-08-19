import threading



class FoodRun(threading.Thread):

    def run(self):
        '''
        开启3个线程同时抓取
        :return:
        '''
        pass


thread_1 = FoodRun()
thread_2 = FoodRun()

thread_1.start()
thread_2.start()

# threading.Thread.join()