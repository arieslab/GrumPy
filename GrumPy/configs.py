import os
import sys
import random
import zipfile
import subprocess
import urllib.request
from threading import Thread
from zipfile import ZipFile
import pathlib
import webbrowser
from time import sleep


def RETURN_SECRET_KEY():
    CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#-&@!?/=*$\\()[]{};:._-'
    secretKey = ''

    current_folder = str(pathlib.Path().absolute()) + '\Redis\\'

    if (os.path.exists('Secret_KEY.txt') == False):
        """
        if (sys.platform == 'win32'):
            redis_link = 'https://github.com/microsoftarchive/redis/releases/download/win-3.0.504/Redis-x64-3.0.504.zip'

            os.mkdir('Redis')

            print('Downloading Redis... ')

            file_name, headers = urllib.request.urlretrieve(redis_link, "redis.zip")

            print('Redis download finished! ')

            print('Extracting Redis zip... ')

            with ZipFile(file_name, 'r') as zip:
                zip.extractall(current_folder)

            print('Redis extracted')

            os.remove("redis.zip")
        """

        for i in range(1, 50, 1):
            secretKey += random.choice(CHARS)

        arq = open('Secret_Key.txt', 'w')
        arq.write(secretKey)
        arq.close()

    else:
        arq = open('Secret_Key.txt', 'r')
        secretKey = arq.read()
        arq.close()


    run_redis = 'start ' + current_folder

    exec_redis = str(pathlib.Path().absolute()) + '\Redis\\redis-server.exe'

    run_redis_thread = Thread(target=iniateRedis, args=(exec_redis,))

    run_redis_thread.start()
    #run_redis_thread.join()
    """
    if (sys.platform == 'win32'):
       chrome_thread = Thread(target=runBrowser, args=('Chrome',))
       chrome_thread.start()
       print("Entrei para abrir o Chrome")
    """
    return secretKey


def iniateRedis(path):
    run_redis = 'start ' + path

    subprocess.call(run_redis, shell=True)

def runBrowser(browser):
    if(browser == 'Chrome'):
        #ChromePath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        grumpy_url = 'http://127.0.0.1:8000/'
        sleep(5)
        webbrowser.open(grumpy_url, new = 0, autoraise=True)

    elif(browser == 'Firefox'):
        pass
    elif(browser == 'Edge'):
        pass