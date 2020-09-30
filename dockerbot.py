from loguru import logger
import time
import re
import random
import datetime
import telepot
from subprocess import call
import subprocess
import os
import sys
from os import path
from telepot.loop import MessageLoop
from dotenv import load_dotenv
import yaml
import shutil


# get YAML with Configs
with open("/opt/dockerbot/config/config.yml", 'r') as stream:
    try:
        list = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# Vars For https://web.mashov.info
v_MASHOV_NUMBER_OF_KIDS = len(list['mashov'])
if v_MASHOV_NUMBER_OF_KIDS >= 1 and list['mashov']['kid1']['MASHOV_USER_ID_KID'] != None:
    v_MASHOV_NUMBER_OF_KIDS = v_MASHOV_NUMBER_OF_KIDS + 1

def handle(msg):
    config_edu = 1
    config_mashov = 1
    message_id = msg['message_id']
    chat_id = msg['chat']['id']
    command = msg['text']
    logger.info(f"[{message_id}] Got msg: {command}")

    # Reject unauthorized requests
    if str(chat_id) not in os.getenv('ALLOWED_IDS'):
        bot.sendPhoto(
            chat_id, "https://github.com/t0mer/dockerbot/raw/master/No-Trespassing.gif")
        logger.error(f"[{message_id}] Chat id not allowed: {chat_id}")
        return
    #need to fix: so only active parts will show and not all options
    if command == '/?' or command == '/start':
        bot.sendMessage(chat_id, "List of available commands: ")
        if list['edu']['USER_ID'] and list['edu']['USER_KEY'] != None:
            bot.sendMessage(
                chat_id, "/sign_edu or /sign- This command start the sign process at https://parents.education.gov.il ")
        if v_MASHOV_NUMBER_OF_KIDS >= 1 and list['mashov']['kid1']['MASHOV_USER_ID_KID'] != None:
            bot.sendMessage(
                chat_id, "/sign_mashov - This command start the sign process at https://web.mashov.info/students/login ")
        if list['infogan']['BASE_URL'] and list['infogan']['KID_ID'] and list['infogan']['PARENT_NAME'] and list['infogan']['KID_NAME'] and list['infogan']['PARENT_ID']  != None:
            bot.sendMessage(
                chat_id, "/sign_infogan - This command start the sign process at https://www.infogan.co.il/ ")
        if list['webtop']['USER_ID'] and list['webtop']['USER_KEY'] != None:
            bot.sendMessage(
                chat_id, "/sign_webtop - This command start the sign process at https://www.webtop.co.il/v2/? ")
        bot.sendMessage(
            chat_id, "/sign_all - This command starts *All* Configured signing process ")

    if command == '/sign_edu' or command == '/sign':
        if list['edu']['USER_ID'] and list['edu']['USER_KEY'] != None:
            Image = '/opt/dockerbot/images/edu_approval.png'
            try:
                bot.sendMessage(
                    chat_id, "Starting Sign process at https://parents.education.gov.il")
                import Health_Statements
                if Health_Statements.sign(str(list['edu']['USER_ID']), list['edu']['USER_KEY'], Image) == 1:
                    time.sleep(1)
                    bot.sendPhoto(chat_id=chat_id,
                                  photo=open(str(Image), 'rb'))
                    bot.sendMessage(chat_id, "Signed")
                    logger.info(
                        f"[{message_id}] Return result to command {command}. Result image path: {Image}")
                else:
                    bot.sendMessage(
                        chat_id, "Well, Somthing went wrong, please check the logs for more info")
            except Exception as ex:
                logger.exception(
                    f"[{message_id}] Failed to handle command. Msg: {command}")
                bot.sendMessage(chat_id, f"ERROR: {str(ex)}")
        else:
            bot.sendMessage(chat_id, "edu NOT configured")

    if command == '/sign_infogan':
        if list['infogan']['BASE_URL'] and list['infogan']['KID_ID'] and list['infogan']['PARENT_NAME'] and list['infogan']['KID_NAME'] and list['infogan']['PARENT_ID']  != None:
            Image = '/opt/dockerbot/images/infogan_approval.png'
            try:
                bot.sendMessage(
                    chat_id, "Starting Sign process at https://https://campaign.infogan.co.il/")
                import Infogan_Health_Statements
                if Infogan_Health_Statements.sign(list['infogan']['PARENT_NAME'], str(list['infogan']['PARENT_ID']),  list['infogan']['KID_NAME'], str(list['infogan']['KID_ID']), list['infogan']['BASE_URL'], Image) == 1:
                    bot.sendPhoto(chat_id=chat_id, photo=open(str(Image), 'rb'))
                    time.sleep(1)
                    os.remove(str(Image))
                    logger.info(f"[{message_id}] Return result to command {command}. Result image path: {Image}")
                    bot.sendMessage(chat_id, "Signed")
                else:
                    bot.sendMessage(chat_id, "Well, Somthing went wrong, please check the logs for more info")
            except Exception as ex:
                logger.exception(
                    f"[{message_id}] Failed to handle command. Msg: {command}")
                bot.sendMessage(chat_id, f"ERROR: {str(ex)}")
        else:
            bot.sendMessage(chat_id, "infogan NOT configured")

    if command == '/sign_webtop':
        if list['webtop']['USER_ID'] and list['webtop']['USER_KEY'] != None:
            try:
                Image = '/opt/dockerbot/images/webtop_approval.png'
                import Webtop_Health_Statements
                if Webtop_Health_Statements.sign(list['webtop']['USER_ID'], list['webtop']['USER_KEY'], Image) == 1:
                    time.sleep(2)
                    bot.sendPhoto(chat_id=chat_id, photo=open(str(Image), 'rb'))
                    logger.info(f"[{message_id}] Return result to command {command}. Result image path: {Image}")
                    bot.sendMessage(chat_id, "Signed")
                else:
                    bot.sendMessage(chat_id, "Well, Somthing went wrong, please check the logs for more info")
            except Exception as ex:
                logger.exception(f"[{message_id}] Failed to handle command. Msg: {command}")
                bot.sendMessage(chat_id, f"ERROR: {str(ex)}")
        else:
            bot.sendMessage(chat_id, "webtop NOT configured")
    if command == '/sign_mashov':
        if v_MASHOV_NUMBER_OF_KIDS >= 1 and list['mashov']['kid1']['MASHOV_USER_ID_KID'] != None:
            try:
                if v_MASHOV_NUMBER_OF_KIDS >= 1 and list['mashov']['kid1']['MASHOV_USER_ID_KID'] != None:
                    for Mashov_Kid_Number in range(1, v_MASHOV_NUMBER_OF_KIDS, 1):
                        if list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_ID_KID'] and list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_PWD_KID'] and list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_SCHOOL_ID_KID'] != None:
                            bot.sendMessage(chat_id,"Starting Sign process at https://web.mashov.info/students/login for Kid Number: " + str(Mashov_Kid_Number))
                            Prep_Switch_MASHOV_USER_DICT_ID_KID = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_ID_KID']
                            Prep_Switch_MASHOV_USER_DICT_ID_PWD = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_PWD_KID']
                            Prep_Switch_MASHOV_USER_DICT_ID_SCHOOL_ID = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_SCHOOL_ID_KID']                     
                            subprocess.check_output(['python', '/opt/dockerbot/Mashov_Health_Statements.py', '-u', Prep_Switch_MASHOV_USER_DICT_ID_KID, '-p', Prep_Switch_MASHOV_USER_DICT_ID_PWD , '-s', Prep_Switch_MASHOV_USER_DICT_ID_SCHOOL_ID, '-kn', str(Mashov_Kid_Number)])
                else:
                    bot.sendMessage(chat_id, "mashov NOT configured")
                    config_mashov = 0

                for file in os.listdir("/opt"):
                    if file.endswith(".png") and file.startswith("mashovkid"):
                        Image = os.path.join("/opt", file)
                        bot.sendPhoto(chat_id=chat_id, photo=open(str(Image), 'rb'))
                        os.remove(str(Image))
                        logger.info(f"[{message_id}] Return result to command {command}. Result image path: {Image}")
                if config_mashov != 0:
                    bot.sendMessage(chat_id, "Signed")
            except Exception as ex:
                logger.exception(f"[{message_id}] Failed to handle command. Msg: {command}")
                bot.sendMessage(chat_id, f"ERROR: {str(ex)}")
        else:
            bot.sendMessage(chat_id, "mashov NOT configured")
    msg = f"Done message handling: {command}"
    logger.info(f"[{message_id}] {msg}")


    if command == '/sign_all':
        if list['edu']['USER_ID'] and list['edu']['USER_KEY'] != None:
            Image = '/opt/dockerbot/images/edu_approval.png'
            try:
                if list['edu']['USER_ID'] != None:
                    bot.sendMessage(
                        chat_id, "Starting Sign process at https://parents.education.gov.il")
                    import Health_Statements
                    if Health_Statements.sign(str(list['edu']['USER_ID']), list['edu']['USER_KEY'], Image) == 1:
                        time.sleep(1)
                        bot.sendPhoto(chat_id=chat_id,
                                      photo=open(str(Image), 'rb'))
                        bot.sendMessage(chat_id, "Signed")
                        logger.info(
                            f"[{message_id}] Return result to command {command}. Result image path: {Image}")
                    else:
                        bot.sendMessage(
                            chat_id, "Well, Somthing went wrong, please check the logs for more info")
                else:
                    bot.sendMessage(chat_id, "edu NOT configured")
                    config_edu = 0
            except Exception as ex:
                logger.exception(
                    f"[{message_id}] Failed to handle command. Msg: {command}")
                bot.sendMessage(chat_id, f"ERROR: {str(ex)}")
        if v_MASHOV_NUMBER_OF_KIDS >= 1 and list['mashov']['kid1']['MASHOV_USER_ID_KID'] != None:
             try:
                 if v_MASHOV_NUMBER_OF_KIDS >= 1 and list['mashov']['kid1']['MASHOV_USER_ID_KID'] != None:
                     for Mashov_Kid_Number in range(1, v_MASHOV_NUMBER_OF_KIDS, 1):
                         bot.sendMessage(chat_id,"Starting Sign process at https://web.mashov.info/students/login for Kid Number: " + str(Mashov_Kid_Number))
                         Prep_Switch_MASHOV_USER_DICT_ID_KID = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_ID_KID']
                         Prep_Switch_MASHOV_USER_DICT_ID_PWD = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_PWD_KID']
                         Prep_Switch_MASHOV_USER_DICT_ID_SCHOOL_ID = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_SCHOOL_ID_KID']                     
                         subprocess.check_output(['python', '/opt/dockerbot/Mashov_Health_Statements.py', '-u', Prep_Switch_MASHOV_USER_DICT_ID_KID, '-p', Prep_Switch_MASHOV_USER_DICT_ID_PWD , '-s', Prep_Switch_MASHOV_USER_DICT_ID_SCHOOL_ID, '-kn', str(Mashov_Kid_Number)])
                 else:
                     bot.sendMessage(chat_id, "mashov NOT configured")
                     config_mashov = 0

                 for file in os.listdir("/opt"):
                     if file.endswith(".png") and file.startswith("mashovkid"):
                         Image = os.path.join("/opt", file)
                         bot.sendPhoto(chat_id=chat_id, photo=open(str(Image), 'rb'))
                         os.remove(str(Image))
                         logger.info(f"[{message_id}] Return result to command {command}. Result image path: {Image}")
                 if config_mashov != 0:
                     bot.sendMessage(chat_id, "Signed")
             except Exception as ex:
                 logger.exception(f"[{message_id}] Failed to handle command. Msg: {command}")
                 bot.sendMessage(chat_id, f"ERROR: {str(ex)}")
        if list['infogan']['BASE_URL'] and list['infogan']['KID_ID'] and list['infogan']['PARENT_NAME'] and list['infogan']['KID_NAME'] and list['infogan']['PARENT_ID']  != None:
            Image = '/opt/dockerbot/images/infogan_approval.png'
            try:
                bot.sendMessage(
                    chat_id, "Starting Sign process at https://https://campaign.infogan.co.il/")
                import Infogan_Health_Statements
                if Infogan_Health_Statements.sign(list['infogan']['PARENT_NAME'], str(list['infogan']['PARENT_ID']),  list['infogan']['KID_NAME'], str(list['infogan']['KID_ID']), list['infogan']['BASE_URL'], Image) == 1:
                    bot.sendPhoto(chat_id=chat_id, photo=open(str(Image), 'rb'))
                    time.sleep(1)
                    os.remove(str(Image))
                    logger.info(f"[{message_id}] Return result to command {command}. Result image path: {Image}")
                    bot.sendMessage(chat_id, "Signed")
                else:
                    bot.sendMessage(chat_id, "Well, Somthing went wrong, please check the logs for more info")
            except Exception as ex:
                logger.exception(
                    f"[{message_id}] Failed to handle command. Msg: {command}")
                bot.sendMessage(chat_id, f"ERROR: {str(ex)}")
        if list['edu']['USER_ID'] and list['edu']['USER_KEY'] != None:
            try:
                Image = '/opt/dockerbot/images/webtop_approval.png'
                import Webtop_Health_Statements
                if Webtop_Health_Statements.sign(list['edu']['USER_ID'], list['edu']['USER_KEY'], Image) == 1:
                    time.sleep(2)
                    bot.sendPhoto(chat_id=chat_id, photo=open(str(Image), 'rb'))
                    logger.info(f"[{message_id}] Return result to command {command}. Result image path: {Image}")
                    bot.sendMessage(chat_id, "Signed")
                else:
                    bot.sendMessage(chat_id, "Well, Somthing went wrong, please check the logs for more info")
            except Exception as ex:
                logger.exception(f"[{message_id}] Failed to handle command. Msg: {command}")
                bot.sendMessage(chat_id, f"ERROR: {str(ex)}")


bot = telepot.Bot(os.getenv('API_KEY'))

MessageLoop(bot, handle).run_as_thread()

logger.info('I am listening...')

while 1:
    time.sleep(10)
    #check Conifg is existed
    original = r'/etc/config.yml'
    target = r'/opt/dockerbot/config/config.yml'

    if os.path.isfile(target):
        continue
    else:
        shutil.copyfile(original, target)
        logger.error("Recoverd Config to /opt/dockerbot/config/")