*Please :star: this repo if you find it useful*

<p align="left"><br>
<a href="https://www.paypal.com/paypalme/techblogil?locale.x=he_IL" target="_blank"><img src="http://khrolenok.ru/support_paypal.png" alt="PayPal" width="250" height="48"></a>
</p>



# Botvid-19

Botvid-19 is a [Telepot](https://telepot.readthedocs.io/en/latest/) and selenium  powered, easy to use Telegram bot for signing Covid-19 digital health statements.


#### Credits:
=======

- [Adam Russak](https://github.com/AdamRussak) for working with me on this project and writing the selenium part


## Usage

#### docker-compose from hub
```yaml
version: "3.7"

services:
  havid-19:
    image: techblog/botid-19
    container_name: botid-19
    restart: always
    labels:
      - "com.ouroboros.enable=true"
    environment:
      - API_KEY= #Telegram BOT API
      - ALLOWED_IDS= #Your Telegram ID (Get is using @myidbot)
   ports:
      - "6700:6700"
```

Replace API_KEY with your bot token. if you do not have existing bot you can create one
using the instruction in this article:
[Bots: An introduction for developers](https://core.telegram.org/bots) 

In order to secure the bot and block unwanted calls from Unauthorized users add your allowd Id's with comma separated values into ALLOWED_IDS
environmet. in order to get your id use @myidbot in telegram and send the /getid command. the result will be your ID:

[![Telegram Bot Integration](https://raw.githubusercontent.com/t0mer/Botvid-19/master/Botvid-19.png "Telegram Bot Integration")](https://raw.githubusercontent.com/t0mer/Botvid-19/master/Botvid-19.png "Telegram Bot Integration")

Please fill in all parameters in the file ./Botvid19.env | Please also fill 1 for the websites you want to sign the health statements on
      - SIGN_WEBSITE_EDUCATION_GOV_IL=0 # 1 for Yes  | to sign at website: https://parents.education.gov.il/prhnet/parents/rights-obligations-regulations/health-statement-kindergarden
      - SIGN_WEBSITE_MASHOV=0 # 1 for Yes | to sign at website: https://web.mashov.info/students/login
      - USER_ID= #parents.education.gov.il portal user
      - USER_KEY= #parents.education.gov.il portal password
      - MASHOV_NUMBER_OF_KIDS=0 # Please enter number of kids on Mashov site , For example: 3
      - MASHOV_USER_ID_KID1= # Please enter login information inside '" "' , For example: '"123456789"'
      - MASHOV_USER_PWD_KID1= # Please enter login information inside '" "' , For example: '"Pa$$w0rd"'
      - MASHOV_SCHOOL_ID_KID1= # Please enter School number inside '" "', can be extracted from URL https://web.mashov.info/students/login , For example: '"123456"'
      - MASHOV_USER_ID_KID2=
      - MASHOV_USER_PWD_KID2=
      - MASHOV_SCHOOL_ID_KID2=
...       

In order to sign the statement, open your browser and nevigate to your container ip address with port 6700:
http://Server_Ip_Address:6700/sign.
The signing process takes about 8-10 seconds and in the ens you'll get a success message.

In oreder to get the image with the signing details nevigate to your container ip address with port 6700:
http://Server_Ip_Address:6700/statement.



# Donation
<br>
If you find this project helpful, you can give me a cup of coffee :) 

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=8CGLEHN2NDXDE)
