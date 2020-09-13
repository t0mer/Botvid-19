from loguru import logger
import time, re, random, datetime, telepot
from subprocess import call
import subprocess, os, sys
from telepot.loop import MessageLoop

env_file = '/opt/Botvid19.env'

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

    if command == '/?':
        bot.sendMessage(chat_id,"List of available commands: ")    
        bot.sendMessage(chat_id,"/sign-edu - This command start the sign process at https://parents.education.gov.il ")   
        bot.sendMessage(chat_id,"/sign-mashov - This command start the sign process at https://web.mashov.info/students/login ")  
        bot.sendMessage(chat_id,"/sign-all - This command start the sign process at all configured websites ")          

    if command == '/sign':  # For legacy sign command -> will refer to /commands
        bot.sendMessage(chat_id,"This command was depreciated, kindly use /? to list all available commands")       
    
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

    if command == '/showsetup':  
        bot.sendMessage(chat_id,"This is the current ENV file parameters: ")     
        file_open = open(env_file, "r") 
        for line in file_open:
           bot.sendMessage(chat_id,line) 
        file_open.close()

    if command == '/setup':  
        bot.sendMessage(chat_id,"Welcome to the parameters setup: ") 
        bot.sendMessage(chat_id,"Show current parameters from Botvid19.env file - write /showsetup")    
        bot.sendMessage(chat_id,"Enable Signing at parents.education.gov.il - write /setup_enable_sign_edu")     
        bot.sendMessage(chat_id,"Disable Signing at parents.education.gov.il - write /setup_disable_sign_edu")
        bot.sendMessage(chat_id,"Enable Signing at web.mashov.info - write /setup_enable_sign_mashov")     
        bot.sendMessage(chat_id,"Disable Signing at web.mashov.info - write /setup_disable_sign_mashov")
        bot.sendMessage(chat_id,"Change Mashov number of kids to sign - write /setup_edu_site_username=username | for example /setup_edu_site_password=123456")
        bot.sendMessage(chat_id,"Change Mashov number of kids to sign - write /setup_edu_site_password=password | for example /setup_edu_site_password=123456")
        bot.sendMessage(chat_id,"Change Mashov number of kids to sign - write /setup_mashov_number_of_kids=number | for example /setup_mashov_number_of_kids=1")


    if command == '/setup_enable_sign_edu': 
        bot.sendMessage(chat_id,"Enabling signing at parents.education.gov.il...") 
        file_open = open(env_file, "rt")
        data = file_open.read()
        data = data.replace('SIGN_WEBSITE_EDUCATION_GOV_IL=0', 'SIGN_WEBSITE_EDUCATION_GOV_IL=1')
        file_open.close()
        file_open = open(env_file, "wt")
        file_open.write(data)
        flle_open.close()

    if command == '/setup_disable_sign_edu': 
        bot.sendMessage(chat_id,"Disabling signing at parents.education.gov.il...") 
        file_open = open(env_file, "rt")
        data = file_open.read()
        data = data.replace('SIGN_WEBSITE_EDUCATION_GOV_IL=1', 'SIGN_WEBSITE_EDUCATION_GOV_IL=0')
        file_open.close()
        file_open = open(env_file, "wt")
        file_open.write(data)
        flle_open.close()

    if command == '/setup_enable_sign_mashov':  
        bot.sendMessage(chat_id,"Enabling signing at web.mashov.info...") 
        file_open = open(env_file, "rt")
        data = file_open.read()
        data = data.replace('SIGN_WEBSITE_MASHOV=0', 'SIGN_WEBSITE_MASHOV=1')
        file_open.close()
        file_open = open(env_file, "wt")
        file_open.write(data)
        flle_open.close()

    if command == '/setup_disable_sign_mashov':  
        bot.sendMessage(chat_id,"Disabling signing at web.mashov.info...") 
        file_open = open(env_file, "rt")
        data = file_open.read()
        data = data.replace('SIGN_WEBSITE_MASHOV=1', 'SIGN_WEBSITE_MASHOV=0')
        file_open.close()
        file_open = open(env_file, "wt")
        file_open.write(data)
        flle_open.close()


    if '/setup_mashov_number_of_kids=' in command:  
        split_mashov_number_of_kids = command.split("=")
        new_mashov_number_of_kids = split_mashov_number_of_kids[1]
        bot.sendMessage(chat_id,"Updating Mashov amount of kids to sign to: "+new_mashov_number_of_kids)
        v_NEW_env_mashov_number_of_kids = 'MASHOV_NUMBER_OF_KIDS='+new_mashov_number_of_kids
        file_open = open(env_file, "r")
        # locate current number of kids in env file
        for line in file_open:
            if 'MASHOV_NUMBER_OF_KIDS=' in line:
                x = line.split(" #")
                y = x[0].split("=")
                current_num = y[1]
        current_string = 'MASHOV_NUMBER_OF_KIDS='+current_num
        file_open.close()
        file_open = open(env_file, "rt")
        data = file_open.read()        
        data = data.replace(current_string,v_NEW_env_mashov_number_of_kids)
        file_open.close()
        file_open = open(env_file, "wt")
        file_open.write(data)
        file_open.close()
    
    if '/setup_edu_site_username=' in command:  
        split_command = command.split("=")
        split2_command = split_command[1]
        bot.sendMessage(chat_id,"Updating edu username to: "+split2_command)
        v_NEW_env_parameter = 'USER_ID='+'"'+split2_command+'"'
        file_open = open(env_file, "r")
        # locate current number of kids in env file
        for line in file_open:
            if 'USER_ID=' in line:
                x = line.split(" #")
                y = x[0].split("=")
                current_num = y[1]
        current_string = 'USER_ID='+current_num
        file_open.close()
        file_open = open(env_file, "rt")
        data = file_open.read()        
        data = data.replace(current_string,v_NEW_env_parameter)
        file_open.close()
        file_open = open(env_file, "wt")
        file_open.write(data)
        file_open.close()  

    if '/setup_edu_site_password=' in command:  
        split_command = command.split("=")
        split2_command = split_command[1]
        bot.sendMessage(chat_id,"Updating edu username to: "+split2_command)
        v_NEW_env_parameter = 'USER_KEY='+'"'+split2_command+'"'
        file_open = open(env_file, "r")
        # locate current number of kids in env file
        for line in file_open:
            if 'USER_KEY=' in line:
                x = line.split(" #")
                y = x[0].split("=")
                current_num = y[1]
        current_string = 'USER_KEY='+current_num
        file_open.close()
        file_open = open(env_file, "rt")
        data = file_open.read()        
        data = data.replace(current_string,v_NEW_env_parameter)
        file_open.close()
        file_open = open(env_file, "wt")
        file_open.write(data)
        file_open.close()  

    if '/setup_mashov_kid1_username=' in command:  
        split_command = command.split("=")
        split2_command = split_command[1]
        bot.sendMessage(chat_id,"Updating edu username to: "+split2_command)
        v_NEW_env_parameter = 'MASHOV_USER_ID_KID1='+'"'+split2_command+'"'
        file_open = open(env_file, "r")
        # locate current number of kids in env file
        for line in file_open:
            if 'MASHOV_USER_ID_KID1=' in line:
                x = line.split(" #")
                y = x[0].split("=")
                current_num = y[1]
        current_string = 'MASHOV_USER_ID_KID1='+current_num
        file_open.close()
        file_open = open(env_file, "rt")
        data = file_open.read()        
        data = data.replace(current_string,v_NEW_env_parameter)
        file_open.close()
        file_open = open(env_file, "wt")
        file_open.write(data)
        file_open.close()  


    msg = f"Done message handling: {command}"
    logger.info(f"[{message_id}] {msg}")


bot = telepot.Bot(os.getenv('API_KEY'))

MessageLoop(bot, handle).run_as_thread()

logger.info('I am listening...')
 
while 1:
    time.sleep(10)
