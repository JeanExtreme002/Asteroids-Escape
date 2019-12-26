import time


class Timer(object):

    def start(self):

        self.__start = time.time()
    
    
    def get(self, format_ = "%M:%S"):

        current_time = time.time()
        return time.strftime(format_, time.localtime(current_time - self.__start))
