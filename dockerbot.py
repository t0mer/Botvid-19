from loguru import logger
import time, re, random, datetime, telepot
from subprocess import call
import subprocess, os, sys
from telepot.loop import MessageLoop

#Vars for Selenium covid kids approval
user_id = os.getenv('USER_ID')
user_password = os.getenv('USER_KEY') 


def handle(msg):
    message_id = str(msg['message_id'])

    logger.info(f"[{message_id}] Got msg: {msg}")

    chat_id = msg['chat']['id']
    command = msg['text']
    
    if str(chat_id) not in os.getenv('ALLOWED_IDS'):
        bot.sendPhoto(chat_id, "https://github.com/t0mer/dockerbot/raw/master/No-Trespassing.gif")
        logger.error(f"[{message_id}] Chat id not allowed: {chat_id}")
        return 

    logger.info(f"[{message_id}] Got command: {command}")

    if command == '/sign':
        v_Kid = "sign"

        try:
            subprocess.check_output(['python', '/etc/Health_Statements.py', '-u', user_id, '-p', user_password, '-k', v_Kid, '-m', message_id])
            
            image_file = f"/opt/Approval_form_{message_id}.png"

            bot.sendPhoto(chat_id=chat_id, photo=open(image_file, 'rb'))
            
            os.remove(image_file)
            
            logger.info(f"[{message_id}] Return result to command {command}. Result image path: {image_file}")

            bot.sendMessage(chat_id, "Signed")
        except Exception as ex:
            logger.exception(f"[{message_id}] Failed to handle command. Msg: {msg}")

            bot.sendMessage(chat_id, f"ERROR: {str(ex)}")

    msg = f"Done message handling: {command}"

    logger.info(f"[{message_id}] {msg}")


bot = telepot.Bot(os.getenv('API_KEY'))

MessageLoop(bot, handle).run_as_thread()

logger.info('I am listening...')
 
while 1:
    time.sleep(10)
