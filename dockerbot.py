from loguru import logger
import time, re, random, datetime, telepot
from subprocess import call
import subprocess, os, sys
from telepot.loop import MessageLoop
import yaml
import shutil

#get YAML with Configs
with open("/opt/config/config.yml", 'r') as stream:
    try:
        list = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


#Vars for Selenium covid kids approval
v_UserId = list['edu']['USER_ID']
v_UserKey = list['edu']['USER_KEY']

#For Mashov
v_MASHOV_NUMBER_OF_KIDS = len(list['mashov'])
if v_MASHOV_NUMBER_OF_KIDS >= 1 and list['mashov']['kid1']['MASHOV_USER_ID_KID'] != None:
    v_MASHOV_NUMBER_OF_KIDS = v_MASHOV_NUMBER_OF_KIDS + 1


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

    if command == '/?':
        bot.sendMessage(chat_id,"List of available commands: ")    
        bot.sendMessage(chat_id,"/sign_edu - This command start the sign process at https://parents.education.gov.il ")   
        bot.sendMessage(chat_id,"/sign_mashov - This command start the sign process at https://web.mashov.info/students/login ")  
        bot.sendMessage(chat_id,"/sign_all - This command start the sign process at all configured websites ")          

    if command == '/sign':  # For legacy sign command -> will refer to /commands
        bot.sendMessage(chat_id,"This command was depreciated, kindly use /? to list all available commands")       
    
    if command == '/sign_all':
        v_Kid = "sign"
        try:
            if list['edu']['USER_ID'] != None:
                bot.sendMessage(chat_id,"Starting Sign process at https://parents.education.gov.il")
                subprocess.check_output(['python', '/opt/dockerbot/Health_Statements.py', '-u', v_UserId, '-p', v_UserKey, '-k', v_Kid])

            if v_MASHOV_NUMBER_OF_KIDS >= 1 and list['mashov']['kid1']['MASHOV_USER_ID_KID'] != None:
                for Mashov_Kid_Number in range(1, v_MASHOV_NUMBER_OF_KIDS, 1):
                    bot.sendMessage(chat_id,"Starting Sign process at https://web.mashov.info/students/login for Kid Number -" + str(Mashov_Kid_Number))
                    Prep_Switch_MASHOV_USER_DICT_ID_KID = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_ID_KID']
                    Prep_Switch_MASHOV_USER_DICT_ID_PWD = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_PWD_KID']
                    Prep_Switch_MASHOV_USER_DICT_ID_SCHOOL_ID = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_SCHOOL_ID_KID']
                    subprocess.check_output(['python', '/opt/dockerbot/Mashov_Health_Statements.py', '-u', Prep_Switch_MASHOV_USER_DICT_ID_KID, '-p', Prep_Switch_MASHOV_USER_DICT_ID_PWD , '-s', Prep_Switch_MASHOV_USER_DICT_ID_SCHOOL_ID, '-kn', str(Mashov_Kid_Number)])

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


    if command == '/sign_edu':
        v_Kid = "sign"
        try:
            if list['edu']['USER_ID'] != None:
                bot.sendMessage(chat_id,"Starting Sign process at https://parents.education.gov.il")
                subprocess.check_output(['python', '/opt/dockerbot/Health_Statements.py', '-u', v_UserId, '-p', v_UserKey, '-k', v_Kid])

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


    if command == '/sign_mashov':
        try:
            if v_MASHOV_NUMBER_OF_KIDS >= '1' and list['mashov']['kid1']['MASHOV_USER_ID_KID'] != None:
                for Mashov_Kid_Number in range(1, v_MASHOV_NUMBER_OF_KIDS, 1):
                    bot.sendMessage(chat_id,"Starting Sign process at https://web.mashov.info/students/login for Kid Number -" + str(Mashov_Kid_Number))
                    Prep_Switch_MASHOV_USER_DICT_ID_KID = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_ID_KID']
                    Prep_Switch_MASHOV_USER_DICT_ID_PWD = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_USER_PWD_KID']
                    Prep_Switch_MASHOV_USER_DICT_ID_SCHOOL_ID = list['mashov']['kid'+str(Mashov_Kid_Number)]['MASHOV_SCHOOL_ID_KID']
                    subprocess.check_output(['python', '/opt/dockerbot/Mashov_Health_Statements.py', '-u', Prep_Switch_MASHOV_USER_DICT_ID_KID, '-p', Prep_Switch_MASHOV_USER_DICT_ID_PWD , '-s', Prep_Switch_MASHOV_USER_DICT_ID_SCHOOL_ID, '-kn', str(Mashov_Kid_Number)])

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
    #check Conifg is existed
    original = r'/etc/config.yml'
    target = r'/opt/config/config.yml'
    if os.path.isfile(target):
        logger.info("Config file exists on /opt/config")
    else:
        shutil.copyfile(original, target)
        logger.info("Copyed Config to /opt/config")
