from loguru import logger
import time, re, random, datetime, telepot, os, sys
from subprocess import call
import subprocess, yaml, shutil
from os import path
from telepot.loop import MessageLoop
from dotenv import load_dotenv

configfile="/opt/dockerbot/config/config.yml"
original_configfile = r'/etc/config.yml'


def copyConfig():
    if not os.path.exists(configfile):
        shutil.copyfile(original_configfile, configfile)


copyConfig()

# Load Configuration
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
    message_id = str(msg['message_id'])
    chat_id = msg['chat']['id']
    _command = command = str(msg['text'])
    logger.info("{message_id} Got msg: {command}")

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
                bot.sendMessage(
                    chat_id, "Starting Sign process at https://www.webtop.co.il/mobilev2/?")
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
        Image = '/opt/dockerbot/images/mashov_approval_'
        if v_MASHOV_NUMBER_OF_KIDS >= 1 and list['mashov']['kid1']['MASHOV_USER_ID_KID'] != None:
            try:
                import Mashov_Health_Statements
                if v_MASHOV_NUMBER_OF_KIDS >= 1 and list['mashov']['kid1']['MASHOV_USER_ID_KID'] != None:
                    for Mashov_Kid_Number in range(1, v_MASHOV_NUMBER_OF_KIDS, 1):
                        if list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_ID_KID'] and list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_PWD_KID'] and list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_SCHOOL_ID_KID'] != None:
                            bot.sendMessage(chat_id,"Starting Sign process at https://web.mashov.info/students/login for Kid Number: " + str(Mashov_Kid_Number))
                            Prep_Switch_MASHOV_USER_DICT_ID_KID = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_ID_KID']
                            Prep_Switch_MASHOV_USER_DICT_ID_PWD = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_PWD_KID']
                            Prep_Switch_MASHOV_USER_DICT_ID_SCHOOL_ID = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_SCHOOL_ID_KID']                     
                            Mashov_Health_Statements.sign(Prep_Switch_MASHOV_USER_DICT_ID_KID, Prep_Switch_MASHOV_USER_DICT_ID_PWD, Prep_Switch_MASHOV_USER_DICT_ID_SCHOOL_ID, str(Mashov_Kid_Number), Image + str(Mashov_Kid_Number) + ".png")
                else:
                    bot.sendMessage(chat_id, "mashov NOT configured")
                    config_mashov = 0

                for file in os.listdir("/opt/dockerbot/images"):
                    if file.endswith(".png") and file.startswith("mashov"):
                        Image = os.path.join("/opt/dockerbot/images", file)
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

bot = telepot.Bot(os.getenv('API_KEY'))
MessageLoop(bot, handle).run_as_thread()
logger.info('I am listening...')


while 1:
    time.sleep(10)
    if os.path.isfile(configfile):
        continue
    else:
        copyConfig()
        logger.error("Recoverd Config to /opt/dockerbot/config/")