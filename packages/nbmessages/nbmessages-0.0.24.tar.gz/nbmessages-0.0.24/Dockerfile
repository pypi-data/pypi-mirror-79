# Dockerfile used for DEVELOPMENT environment only

FROM jupyter/datascience-notebook:latest

USER root

RUN mkdir -p /srv/nbmessages/admin
# for testing, only root can modify both message boards (at least by default)
RUN chmod -R 0755 /srv/nbmessages

COPY . /opt/nbmessages

WORKDIR /opt/nbmessages

# install nbmessages
RUN rm -rf build dist
RUN python3 setup.py bdist_wheel
RUN pip install dist/*.whl

RUN pip install twine

RUN jupyter serverextension enable --sys-prefix --py nbmessages
RUN jupyter nbextension install --sys-prefix --py nbmessages
RUN jupyter nbextension enable --user message/main --section=tree
RUN jupyter nbextension enable --user admin/main --section=tree
RUN ln -fs /usr/share/zoneinfo/America/Los_Angeles /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

# Chromedriver
RUN apt-get update
RUN apt-get install software-properties-common -y 
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

RUN apt-get clean
RUN apt-get update
RUN apt-get install google-chrome-stable -y

RUN wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver

RUN apt-get install iputils-ping

# for testing purposes, add multiple users
RUN useradd -u 1001 -ms /bin/bash user1
RUN useradd -u 1002 -ms /bin/bash user2
RUN useradd -u 1003 -ms /bin/bash user3

RUN chown -R 1000:1000 /home/jovyan
RUN chmod -R 777 /home/jovyan

ENV START "/opt/conda/bin/jupyter notebook --ip 0.0.0.0 --allow-root --NotebookApp.token=''"