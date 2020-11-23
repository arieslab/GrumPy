import urllib.request
import pathlib
import os
import sys
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

            #run_mongodb = 'start /wait ' + str(pathlib.Path().absolute()) + '\\mongodb-win32-x86_64-windows-4.4.1\\bin\\mongod --dbpath ' + data_folder



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
            subprocess.call('start /wait pip install celery', shell=True)
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


        flag = input('Would you like to perform the database migrations? (Y or N): ')

        if (flag.upper() == 'Y'):
            makemigrations_grumpy = 'start python manage.py makemigrations'
            subprocess.call(makemigrations_grumpy, shell=True)
            migrate_grumpy = 'start python manage.py migrate'
            subprocess.call(migrate_grumpy, shell=True)

        flag = input('Would you like to start App? (Y or N): ')

        if (flag.upper() == 'Y'):
            run_grumpy = 'start python manage.py runserver'
            Grumpy_terminal_thread = Thread(target=starts_grumpy, args=(run_grumpy,))
            Grumpy_terminal_thread.start()

elif(sys.argv[1] == 'Run'):
    if (sys.platform == 'win32'):
        run_redis = 'start /wait ' + str(pathlib.Path().absolute()) + '\Redis\\redis-server.exe'
        Redis_thread = Thread(target=starts_Redis, args=(run_redis,))
        thread_management.append(Redis_thread)
        #Redis_thread.start()

        MongoDB_thread = Thread(target=starts_MongoDB, args=(run_mongodb,))
        thread_management.append(MongoDB_thread)

        #MongoDB_thread.start()

        run_celery = 'start /wait celery -A GrumPy worker -l info --without-gossip --without-mingle --without-heartbeat -Ofair --pool threads'
        Celery_thread = Thread(target=starts_celery, args=(run_celery,))
        thread_management.append(Celery_thread)
        #Celery_thread.start()

        run_grumpy = 'start python manage.py runserver'
        Grumpy_terminal_thread = Thread(target=starts_grumpy, args=(run_grumpy,))
        thread_management.append(Grumpy_terminal_thread)
        #Grumpy_terminal_thread.start()

        for i in thread_management:
            i.start()

        print('To terminate the program close all the opened windows')