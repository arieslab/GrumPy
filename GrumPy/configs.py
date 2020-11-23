import os
import random
import pathlib

def RETURN_SECRET_KEY():
    CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#-&@!?/=*$\\()[]{};:._-'
    secretKey = ''

    current_folder = str(pathlib.Path().absolute()) + '\Redis\\'

    if (os.path.exists('Secret_KEY.txt') == False):
        for i in range(1, 50, 1):
            secretKey += random.choice(CHARS)

        arq = open('Secret_Key.txt', 'w')
        arq.write(secretKey)
        arq.close()

    else:
        arq = open('Secret_Key.txt', 'r')
        secretKey = arq.read()
        arq.close()

    return secretKey
