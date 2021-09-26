FROM codercom/code-server:latest

USER root

#install environment requirements
RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install configparser pymodbus

#install code extensions
#RUN code-server --install-extension ms-python.python

#git
RUN git config --global user.email "robertdiers@gmail.com"
RUN git config --global user.name "Robert Diers"
