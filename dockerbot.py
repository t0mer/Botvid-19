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
v_KidTotal = os.getenv('KIDS_NUM')
#Auto Commmand List
def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    list_of_results = []
    new_line = "\n"
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                if ("/?" not in line and not "o/" in line and not "," in line):
                    command = line
                    number = command.rfind("/")
                    command = command[number:]
                    number = command.rfind("'")
                    command = command[:number]
                    command = command + new_line
                    # If yes, then add the line number & line as a tuple in the list
                    list_of_results.append(command)
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    
    if str(chat_id) not in os.getenv('ALLOWED_IDS'):
        bot.sendPhoto(chat_id,"https://github.com/t0mer/dockerbot/raw/master/No-Trespassing.gif")
        return ""



    print ('Got command: %s')%command
    if command == '/yuval':
        v_Kid = "yuval"
        try:
            subprocess.check_output(['python', '/etc/Health_Staytments.py', '-u', v_UserId, '-p', v_UserKey, '-k', v_Kid, '-n', str(v_KidTotal)])
            for file in os.listdir("/opt"):
                if file.endswith(".png"):
                    Image = os.path.join("/opt", file)
            bot.sendPhoto(chat_id=chat_id, photo=open(str(Image), 'rb'))
        except:
            x = "Error"
            bot.sendMessage(chat_id,x)
    elif command == '/omer':
        v_Kid = "omer"
        try:
            subprocess.check_output(['python', '/etc/Health_Staytments.py', '-u', v_UserId, '-p', v_UserKey, '-k', v_Kid, '-n', str(v_KidTotal)])
            for file in os.listdir("/opt"):
                if file.endswith(".png"):
                    Image = os.path.join("/opt", file)
            bot.sendPhoto(chat_id=chat_id, photo=open(str(Image), 'rb'))
        except:
            x = "Error"
            bot.sendMessage(chat_id,x)
    elif command == '/sign':
        v_Kid = "sign"
        try:
            subprocess.check_output(['python', '/etc/Health_Staytments.py', '-u', v_UserId, '-p', v_UserKey, '-k', v_Kid, '-n', str(v_KidTotal)])
            for file in os.listdir("/opt"):
                if file.endswith(".png"):
                    Image = os.path.join("/opt", file)
            bot.sendPhoto(chat_id=chat_id, photo=open(str(Image), 'rb'))
        except:
            x = "Error"
            bot.sendMessage(chat_id,x)
    elif command == '/?':
        array = search_string_in_file('/opt/dockerbot/dockerbot.py', "/")
        s = "Command List:\n"
        for val in array:
            if ")" not in val:
                s+=str(val)
        x = s
        bot.sendMessage(chat_id,x)

bot = telepot.Bot(os.getenv('API_KEY'))
MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')
 
while 1:
    time.sleep(10)
