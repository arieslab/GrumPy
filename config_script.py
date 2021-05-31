import urllib.request
import pathlib
import os
import sys
import webbrowser
from zipfile import ZipFile
import subprocess
from threading import Thread

thread_management = []

run_mongodb = 'start /wait ' + str(
    pathlib.Path().absolute()) + '\\mongodb-win32-x86_64-windows-4.4.1\\bin\\mongod --dbpath ' + str(
    pathlib.Path().absolute()) + '\\mongodb-win32-x86_64-windows-4.4.1\\bin\\data\\db'

def starts_grumpy(p):
    subprocess.call(p, shell=True)
    print('Grumpy terminal closed')

def starts_Redis(p):
    subprocess.call(p, shell=True)
    print('Redis terminal closed')

def starts_MongoDB(p):
    subprocess.call(p, shell=True)
    print('MongoDB terminal closed')

def starts_celery(p):
    subprocess.call(p, shell=True)
    print('Celery terminal closed')

def starts_browser(p):
    if (flag.upper() == '1'):
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
        webbrowser.get('chrome').open_new("http://localhost:8000")
    elif(flag.upper() == '2'):
        webbrowser.register('edge', None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Microsoft//Edge//Application//msedge.exe"))
        webbrowser.get('edge').open_new("http://localhost:8000")    
    elif(flag.upper() == '3'): 
        webbrowser.register('firefox', None,  webbrowser.BackgroundBrowser('C://Program Files//Mozilla Firefox//firefox.exe'))
        webbrowser.get('firefox').open_new("http://localhost:8000")

    print('Browser closed')

if(sys.argv[1] == 'Install'):
    if (sys.platform == 'win32'):
        flag = input('Would you like to download and install Redis? (Y or N): ')


        if(flag.upper() == 'Y'):
            redis_link = 'https://github.com/microsoftarchive/redis/releases/download/win-3.0.504/Redis-x64-3.0.504.zip'

            current_folder = str(pathlib.Path().absolute()) + '\Redis\\'

            os.mkdir('Redis')

            file_name, headers = urllib.request.urlretrieve (redis_link, "redis.zip")

            print('Redis download finished! ')

            redis_file_target = str(str(current_folder) + str(file_name))

            print('Extracting Redis...')

            with ZipFile(file_name, 'r') as z:
                z.extractall(current_folder)

            print('Redis extracted!')

            os.remove("redis.zip")

        flag = input('Would you like to download and install MongoDB? (Y or N): ')

        if (flag.upper() == 'Y'):
            mongodb_link = 'https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-4.4.1.zip'

            print('Downloading MongoDB...')

            file_name, headers = urllib.request.urlretrieve (mongodb_link, "mongodb.zip")

            print('MongoDB download finished!')

            print('Extracting MongoDB...')

            with ZipFile(file_name, 'r') as z:
                z.extractall()

            print('MongoDB extracted!')

            os.remove("mongodb.zip")

            Dbfolder = str(pathlib.Path().absolute()) + '\\mongodb-win32-x86_64-windows-4.4.1\\bin'
            data_folder = Dbfolder + '\\data'
            os.mkdir(data_folder)
            data_folder = data_folder + '\\db'
            os.mkdir(data_folder)

        flag = input('Would you like to download and install PIP? (Y or N): ')

        if (flag.upper() == 'Y'):
            pip_url = 'https://bootstrap.pypa.io/get-pip.py'
            file_name, headers = urllib.request.urlretrieve(pip_url, "get-pip.py")
            pip_install_string = 'start /wait python ' + file_name
            subprocess.call(pip_install_string, shell=True)
            os.remove("get-pip.py")
            print('PIP installed!')

        
        flag = input('Would you like to download and install the GrumPy dependencies by PIP? (Y or N): ')

        if (flag.upper() == 'Y'):
            print('Installing Celery')
            subprocess.call('start /wait pip install pip install celery==5.0.5', shell=True)
            print('Installing Redis')
            subprocess.call('start /wait pip install redis', shell=True)
            print('Installing Django-celery-results')
            subprocess.call('start /wait pip install django-celery-results', shell=True)
            print('Installing Celery-progress')
            subprocess.call('start /wait pip install celery-progress', shell=True)
            print('Installing Requests')
            subprocess.call('start /wait pip install requests', shell=True)
            print('Installing PyGithub')
            subprocess.call('start /wait pip install pygithub', shell=True)
            print('Installing Django-bootstrap4')
            subprocess.call('start /wait pip install django-bootstrap4', shell=True)
            print('Installing Pymongo')
            subprocess.call('start /wait pip install pymongo', shell=True)
            print('Installing Pytest')
            subprocess.call('start /wait pip install pytest', shell=True)
            print('Installing eventlet')
            subprocess.call('start /wait pip install eventlet', shell=True)
            print('Installing gevent')
            subprocess.call('start /wait pip install gevent', shell=True)
            print('Installing Bootstrap4')
            subprocess.call('start /wait python -m pip install bootstrap4', shell=True)
            print('Installing Requests')
            subprocess.call('start /wait python -m pip install requests', shell=True)
            print('Installing django_forms_bootstrap')
            subprocess.call('start /wait python -m pip install django_forms_bootstrap', shell=True)

        flag = input('Would you like to perform the database migrations? (Y or N): ')

        if (flag.upper() == 'Y'):
            makemigrations_grumpy = 'start python manage.py makemigrations'
            subprocess.call(makemigrations_grumpy, shell=True)
            migrate_grumpy = 'start python manage.py migrate'
            subprocess.call(migrate_grumpy, shell=True)


elif(sys.argv[1] == 'Run'):
    if (sys.platform == 'win32'):
        run_redis = 'start /wait ' + str(pathlib.Path().absolute()) + '\Redis\\redis-server.exe'
        Redis_thread = Thread(target=starts_Redis, args=(run_redis,))
        thread_management.append(Redis_thread)

        MongoDB_thread = Thread(target=starts_MongoDB, args=(run_mongodb,))
        thread_management.append(MongoDB_thread)

        run_celery = 'start /wait celery -A GrumPy worker -l info --without-gossip --without-mingle --without-heartbeat -Ofair --pool threads'
        Celery_thread = Thread(target=starts_celery, args=(run_celery,))
        thread_management.append(Celery_thread)

        run_grumpy = 'start python manage.py runserver'
        Grumpy_terminal_thread = Thread(target=starts_grumpy, args=(run_grumpy,))
        thread_management.append(Grumpy_terminal_thread)

        print('Select your browser')
        print('(1) Chrome')
        print('(2) Edge')
        print('(3) Firefox')

        flag = input('Type the number: ')

        if (flag.upper() == '1'):
            Browser_thread = Thread(target=starts_browser, args=('1',))
        elif(flag.upper() == '2'):
            Browser_thread = Thread(target=starts_browser, args=('2',))
        elif(flag.upper() == '3'):
            Browser_thread = Thread(target=starts_browser, args=('3',))

        thread_management.append(Browser_thread)

        for i in thread_management:
            i.start()

        print('To terminate the program close all the opened windows')