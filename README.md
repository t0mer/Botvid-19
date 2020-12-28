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

### supported platforms:
* [edu](https://parents.education.gov.il)
* [mashov](https://web.mashov.info/students/login)
* [infogan](https://https://campaign.infogan.co.il/)
* [webtop](https://www.webtop.co.il/mobilev2/?)

#### docker-compose from hub
```yaml
version: "3.7"

services:
  botvid:
    image: techblog/botvid-19
    container_name: botvid
    restart: always
    labels:
      - "com.ouroboros.enable=true"
    environment:
      - API_KEY=
      - ALLOWED_IDS=
    volumes:
      - ./botvid/config/:/opt/dockerbot/config

```

Replace API_KEY with your bot token. if you do not have existing bot you can create one
using the instruction in this article:
[Bots: An introduction for developers](https://core.telegram.org/bots) 

In order to secure the bot and block unwanted calls from Unauthorized users add your allowd Id's with comma separated values into ALLOWED_IDS
environmet. in order to get your id use @myidbot in telegram and send the /getid command. the result will be your ID.

Run
```
docker-compose up -d
```
A config file will be created in ./botvid/config/config.yaml

Please fill in the parameters in the file config.yml
```
edu:
    USER_ID: 
    USER_KEY: 
mashov:
#Add Kids Block as needed
#UNused Kid Block should be left empty or removed from file
    kid1:
        MASHOV_USER_ID_KID: 
        MASHOV_USER_PWD_KID: 
        MASHOV_SCHOOL_ID_KID: 
    kid2:
        MASHOV_USER_ID_KID:
        MASHOV_USER_PWD_KID: 
        MASHOV_SCHOOL_ID_KID:
infogan:
    BASE_URL: 
    PARENT_NAME: 
    PARENT_ID: 
    KID_NAME: 
    KID_ID: 
webtop:
    USER_ID: 
    USER_KEY: 
  ```

You may fill only the section that are relevant to you.

Enter the bot in Telegram and run the relevant command:
    `/sign` - all configured commands
    `/sign_mashov` - only Mashov
    `/sign_infogan` - only InfoGan
    `/sign_webtop` - only WebTop
    `/?` or `/start` - show configured settings

You will get the signed form after about 10 seconds.

[![Telegram Bot Integration](https://raw.githubusercontent.com/t0mer/Botvid-19/master/example/images/Botvid-19.png "Telegram Bot Integration")](https://raw.githubusercontent.com/t0mer/Botvid-19/master/Botvid-19.png "Telegram Bot Integration")




# Donation
<br>
If you find this project helpful, you can give me a cup of coffee :) 

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=8CGLEHN2NDXDE)
