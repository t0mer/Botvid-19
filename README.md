# botid-19

botid-19 is a [Telepot](https://telepot.readthedocs.io/en/latest/) and selenium  powerd, easy to use Telegram bot for signing Covid-19 digital health statement.


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
      - USER_ID= #parents.education.gov.il portal user
      - USER_KEY= #parents.education.gov.il portal password
   ports:
      - "6700:6700"
```

Replace API_KEY with your bot token. if you do not have existing bot you can create one
using the instruction in this article:
[Bots: An introduction for developers](https://core.telegram.org/bots) 

In order to secure the bot and block unwanted calls from Unauthorized users add your allowd Id's with comma separated values into ALLOWED_IDS
environmet. in order to get your id use @myidbot in telegram and send the /getid command. the result will be your ID:

[![Home Assistant Integration](https://raw.githubusercontent.com/t0mer/HAvid-19/master/HAvid-19.png "Home Assistant Integration")](https://raw.githubusercontent.com/t0mer/HAvid-19/master/HAvid-19.png "Home Assistant Integration")

In order to sign the statement, open your browser and nevigate to your container ip address with port 6700:
http://Server_Ip_Address:6070/sign.
The signing process takes about 8-10 seconds and in the ens you'll get a success message.

In oreder to get the image with the signing details nevigate to your container ip address with port 6700:
http://Server_Ip_Address:6070/statement.



# Donation
<br>
If you find this project helpful, you can give me a cup of coffee :) 

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=8CGLEHN2NDXDE)
