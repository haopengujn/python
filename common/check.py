#-*- coding: utf-8 -*-

import threading  
import time

num=0

class myThread(threading.Thread):  
    def __init__(self):  
        threading.Thread.__init__(self)  
          
    def run(self):  
    	global num 
        while True:  
        	print num
        	num += 1
        	time.sleep(1) 


def main():
	thread1 = myThread()
	thread1.start()

if __name__=='__main__':
    main()