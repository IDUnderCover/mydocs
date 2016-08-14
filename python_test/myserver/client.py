#!/usr/bin/env python

import requests
import threading


thread_num = 1
URL = 'http://127.0.0.1:9999'
def handler():
    res = requests.get(URL,timeout=1001) 
    print res, threading.current_name()

if __name__ == '__main__':
    threads = [threading.Thread(target=handler) for i in range(thread_num)]  
    
    print 'starting threads'
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
