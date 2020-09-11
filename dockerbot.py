from loguru import logger
import time, re, random, datetime, telepot
from subprocess import call
import subprocess, os, sys
from telepot.loop import MessageLoop

#Vars for Selenium covid kids approval
v_UserId = os.getenv('USER_ID')
v_UserKey = os.getenv('USER_KEY') 

def handle(msg):
    message_id = msg['message_id'] 
    chat_id = msg['chat']['id']
    command = msg['text']
    logger.info(f"[{message_id}] Got msg: {command}")


    
    if str(chat_id) not in os.getenv('ALLOWED_IDS'):
        bot.sendPhoto(chat_id, "https://github.com/t0mer/dockerbot/raw/master/No-Trespassing.gif")
        logger.error(f"[{message_id}] Chat id not allowed: {chat_id}")
        return 

    logger.info(f"[{message_id}] Got command: {command}")

    if command == '/sign':
        v_Kid = "sign"
        try:
            subprocess.check_output(['python', '/etc/Health_Statements.py', '-u', v_UserId, '-p', v_UserKey, '-k', v_Kid])
            for file in os.listdir("/opt"):
                if file.endswith(".png"):
                    Image = os.path.join("/opt", file)
            bot.sendPhoto(chat_id=chat_id, photo=open(str(Image), 'rb'))
            os.remove(str(Image))
            logger.info(f"[{message_id}] Return result to command {command}. Result image path: {Image}")
            bot.sendMessage(chat_id, "Signed")
        except Exception as ex:
            logger.exception(f"[{message_id}] Failed to handle command. Msg: {command}")
            bot.sendMessage(chat_id, f"ERROR: {str(ex)}")

    msg = f"Done message handling: {command}"
    logger.info(f"[{message_id}] {msg}")


bot = telepot.Bot(os.getenv('API_KEY'))

MessageLoop(bot, handle).run_as_thread()

logger.info('I am listening...')
 
while 1:
    time.sleep(10)
