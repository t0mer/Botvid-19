FROM python

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true
ENV API_KEY ""
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8

# Set timezone
RUN echo "Asia/Jerusalem" > /etc/timezone && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Create a default user
RUN groupadd --system automation && \
    useradd --system --create-home --gid automation --groups audio,video automation && \
    mkdir --parents /home/automation/reports && \
    chown --recursive automation:automation /home/automation

# Update the repositories
# Install dependencies
# Install utilities
# Install XVFB and TinyWM
# Install fonts
RUN apt-get -yqq update && \
    apt-get -yqq install gnupg2 && \
    apt-get -yqq install curl unzip && \
    apt-get -yqq install xvfb tinywm && \
    apt-get -yqq install fonts-ipafont-gothic xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic && \
    rm -rf /var/lib/apt/lists/*

# Install Chrome WebDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
    ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

# Install Google Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -yqq update && \
    apt-get -yqq install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Default configuration
ENV DISPLAY :20.0
ENV SCREEN_GEOMETRY "1440x900x24"
ENV CHROMEDRIVER_PORT 4444
ENV CHROMEDRIVER_WHITELISTED_IPS "127.0.0.1"
ENV CHROMEDRIVER_URL_BASE ''
ENV CHROMEDRIVER_EXTRA_ARGS ''

EXPOSE 4444

RUN pip install selenium --no-cache-dir && \
    pip install telepot --no-cache-dir && \
    pip install pyyaml --no-cache-dir && \
    pip install python-dotenv --no-cache-dir && \
    pip install loguru --no-cache-dir && \
    pip install fake_useragent --no-cache-dir
    
RUN mkdir /opt/dockerbot
RUN mkdir /opt/dockerbot/config
RUN mkdir /opt/dockerbot/images

COPY config.yml /opt/dockerbot/config
COPY config.yml /etc
COPY Health_Statements.py /opt/dockerbot
COPY Mashov_Health_Statements.py /opt/dockerbot
COPY Webtop_Health_Statements.py /opt/dockerbot
COPY Infogan_Health_Statements.py /opt/dockerbot
COPY helpers.py /opt/dockerbot
COPY dockerbot.py /opt/dockerbot

VOLUME [ "/opt/config" ]

RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && echo 'export PATH=/opt/chromedriver-${CHROMEDRIVER_VERSION}:$PATH' >> /root/.bashrc && chmod 777 /opt/dockerbot/Health_Statements.py && chmod 777 /opt/dockerbot/Mashov_Health_Statements.py

ENTRYPOINT ["python", "/opt/dockerbot/dockerbot.py"]
