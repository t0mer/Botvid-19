import time
import re
import random
import datetime
import telepot
from subprocess import call
import subprocess
import os
import sys
import docker
from telepot.loop import MessageLoop

#Vars for Selenium covid kids approval
v_UserId = os.getenv('USER_ID')
v_UserKey = os.getenv('USER_KEY') 

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    
    if str(chat_id) not in os.getenv('ALLOWED_IDS'):
        bot.sendPhoto(chat_id,"https://github.com/t0mer/dockerbot/raw/master/No-Trespassing.gif")
        return ""

    print ('Got command: %s')%command
    if command == '/sign':
        v_Kid = "sign"
        try:
            subprocess.check_output(['python', '/etc/Health_Staytments.py', '-u', v_UserId, '-p', v_UserKey, '-k', v_Kid])
            for file in os.listdir("/opt"):
                if file.endswith(".png"):
                    Image = os.path.join("/opt", file)
            bot.sendPhoto(chat_id=chat_id, photo=open(str(Image), 'rb'))
            os.remove(str(Image))
        except:
            x = "Error"
            bot.sendMessage(chat_id,x)


bot = telepot.Bot(os.getenv('API_KEY'))
MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')
 
while 1:
    time.sleep(10)
