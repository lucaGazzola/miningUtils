'''
Created on 12 Dec 2017

@author: Luca G.
'''
import requests
import time
import logging
import os
import subprocess
import ctypes
import psutil

def internet_on():
    try:
        requests.get('http://www.google.com')
        return True
    except: 
        return False
    
if __name__ == "__main__":
    
    no_connection_flag = False
    logger = logging.getLogger('miner')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    hdlr = logging.FileHandler(dir_path+'/log.txt')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)
    process = subprocess.Popen(['start_only_eth.bat'], close_fds=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    
    while True:
        
        if internet_on():
            if no_connection_flag:
                logger.info('connection back, starting miner...')
                no_connection_flag = False
                # start miner
                process = subprocess.Popen(['start_only_eth.bat'],creationflags=subprocess.CREATE_NEW_CONSOLE, close_fds=True)
            logger.info("ok, sleeping...")
            time.sleep(30)
            continue
        else:
            logger.info("no connenction, terminating miner...")
            # terminate miner
            pro = psutil.Process(process.pid)
            for proc in pro.children(recursive=True):
               proc.kill()
            process.kill()
            no_connection_flag = True
            time.sleep(30)
