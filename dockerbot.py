from loguru import logger
import time, re, random, datetime, telepot
from subprocess import call
import subprocess, os, sys
from telepot.loop import MessageLoop

#Which Signing Website
v_SIGN_PARENTS_EDUCATION_GOV_IL = int(os.getenv('SIGN_WEBSITE_EDUCATION_GOV_IL'))
v_SIGN_WEBSITE_MASHOV = int(os.getenv('SIGN_WEBSITE_MASHOV'))

#Vars for Selenium covid kids approval
v_UserId = os.getenv('USER_ID')
v_UserKey = os.getenv('USER_KEY') 

#For Mashov
v_MASHOV_NUMBER_OF_KIDS = os.getenv('MASHOV_NUMBER_OF_KIDS')
v_MASHOV_NUMBER_OF_KIDS = int(v_MASHOV_NUMBER_OF_KIDS)
if v_MASHOV_NUMBER_OF_KIDS != '0':
    v_MASHOV_NUMBER_OF_KIDS = v_MASHOV_NUMBER_OF_KIDS + 1

v_MASHOV_USER_DICT_ID_KID = {}
v_MASHOV_USER_DICT_ID_PWD = {}
v_MASHOV_USER_DICT_ID_SCHOOL_ID = {}


if v_MASHOV_NUMBER_OF_KIDS > 0:
    for Load_Mashov_Kid_Vars in range(1, v_MASHOV_NUMBER_OF_KIDS, 1):
        v_MASHOV_USER_DICT_ID_KID[Load_Mashov_Kid_Vars] = eval(os.getenv('MASHOV_USER_ID_KID'+str(Load_Mashov_Kid_Vars)))
        v_MASHOV_USER_DICT_ID_PWD[Load_Mashov_Kid_Vars] = eval(os.getenv('MASHOV_USER_PWD_KID'+str(Load_Mashov_Kid_Vars)))
        v_MASHOV_USER_DICT_ID_SCHOOL_ID[Load_Mashov_Kid_Vars] = eval(os.getenv('MASHOV_SCHOOL_ID_KID'+str(Load_Mashov_Kid_Vars)))


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

    if command == '/signall':
        v_Kid = "sign"
        try:
            if v_SIGN_PARENTS_EDUCATION_GOV_IL == 1:
                bot.sendMessage(chat_id,"Starting Sign process at https://parents.education.gov.il")
                subprocess.check_output(['python', '/etc/Health_Statements.py', '-u', v_UserId, '-p', v_UserKey, '-k', v_Kid])

            if v_SIGN_WEBSITE_MASHOV == 1:
                if v_MASHOV_NUMBER_OF_KIDS > 0:
                    for Mashov_Kid_Number in range(1, v_MASHOV_NUMBER_OF_KIDS, 1):
                        bot.sendMessage(chat_id,"Starting Sign process at https://web.mashov.info/students/login for Kid Number -" + str(Mashov_Kid_Number))
                        Prep_Switch_MASHOV_USER_DICT_ID_KID = v_MASHOV_USER_DICT_ID_KID[Mashov_Kid_Number]
                        Prep_Switch_MASHOV_USER_DICT_ID_PWD = v_MASHOV_USER_DICT_ID_PWD[Mashov_Kid_Number]
                        Prep_Switch_MASHOV_USER_DICT_ID_SCHOOL_ID = v_MASHOV_USER_DICT_ID_SCHOOL_ID[Mashov_Kid_Number]
                        subprocess.check_output(['python', '/etc/Mashov_Health_Statements.py', '-u', Prep_Switch_MASHOV_USER_DICT_ID_KID, '-p', Prep_Switch_MASHOV_USER_DICT_ID_PWD , '-s', Prep_Switch_MASHOV_USER_DICT_ID_SCHOOL_ID, '-kn', str(Mashov_Kid_Number)])

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


    if command == '/sign-edu':
        v_Kid = "sign"
        try:
            if v_SIGN_PARENTS_EDUCATION_GOV_IL == 1:
                bot.sendMessage(chat_id,"Starting Sign process at https://parents.education.gov.il")
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


    if command == '/sign-mashov':
        try:
            if v_SIGN_WEBSITE_MASHOV == 1:
                if v_MASHOV_NUMBER_OF_KIDS > 0:
                    for Mashov_Kid_Number in range(1, v_MASHOV_NUMBER_OF_KIDS, 1):
                        bot.sendMessage(chat_id,"Starting Sign process at https://web.mashov.info/students/login for Kid Number -" + str(Mashov_Kid_Number))
                        Prep_Switch_MASHOV_USER_DICT_ID_KID = v_MASHOV_USER_DICT_ID_KID[Mashov_Kid_Number]
                        Prep_Switch_MASHOV_USER_DICT_ID_PWD = v_MASHOV_USER_DICT_ID_PWD[Mashov_Kid_Number]
                        Prep_Switch_MASHOV_USER_DICT_ID_SCHOOL_ID = v_MASHOV_USER_DICT_ID_SCHOOL_ID[Mashov_Kid_Number]
                        subprocess.check_output(['python', '/etc/Mashov_Health_Statements.py', '-u', Prep_Switch_MASHOV_USER_DICT_ID_KID, '-p', Prep_Switch_MASHOV_USER_DICT_ID_PWD , '-s', Prep_Switch_MASHOV_USER_DICT_ID_SCHOOL_ID, '-kn', str(Mashov_Kid_Number)])

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
