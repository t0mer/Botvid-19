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
  dockerbot:
    build: 
      context: .
      dockerfile: ./Dockerfile
    container_name: dockerbot
    network_mode: host
    cap_add:
      - NET_ADMIN
    privileged: true
    restart: always
    environment:
      - API_KEY=
      - ALLOWED_IDS=
    volumes:
        - /var/run/docker.sock:/var/run/docker.sock
        - /path/to/config/in/host:/opt/config
```

Replace API_KEY with your bot token. if you do not have existing bot you can create one
using the instruction in this article:
[Bots: An introduction for developers](https://core.telegram.org/bots) 

In order to secure the bot and block unwanted calls from Unauthorized users add your allowd Id's with comma separated values into ALLOWED_IDS
environmet. in order to get your id use @myidbot in telegram and send the /getid command. the result will be your ID:

[![Telegram Bot Integration](https://raw.githubusercontent.com/t0mer/Botvid-19/master/example/images/Botvid-19.png "Telegram Bot Integration")](https://raw.githubusercontent.com/t0mer/Botvid-19/master/Botvid-19.png "Telegram Bot Integration")

Please fill in all parameters in the file ./config.yml
```
edu:
    USER_ID: 
    USER_KEY: 
webtop:
    USER_ID: 
    USER_KEY: 
mashov:
#Add Kids Block as needed (please enclose with "" , for example "123456")
#UNused Kid Block should be commented with # or removed from file
    kid1:
        MASHOV_USER_ID_KID: 
        MASHOV_USER_PWD_KID: 
        MASHOV_SCHOOL_ID_KID: 
    #kid2:
    #    MASHOV_USER_ID_KID: 
    #    MASHOV_USER_PWD_KID: 
    #    MASHOV_SCHOOL_ID_KID: 
infogan:
    BASE_URL: 
    PARENT_NAME: 
    PARENT_ID: 
    KID_NAME: 
    KID_ID: 
  ```


In order to sign the statement, open your browser and nevigate to your container ip address with port 6700:
http://Server_Ip_Address:6700/sign.
The signing process takes about 8-10 seconds and in the ens you'll get a success message.

In oreder to get the image with the signing details nevigate to your container ip address with port 6700:
http://Server_Ip_Address:6700/statement.



# Donation
<br>
If you find this project helpful, you can give me a cup of coffee :) 

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=8CGLEHN2NDXDE)
