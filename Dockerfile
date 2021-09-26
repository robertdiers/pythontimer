FROM python:slim-buster

USER root

RUN apt update
RUN apt -y upgrade
RUN pip3 install configparser pymodbus

# copy files
COPY kostal_idm.py /app/kostal_idm.py
COPY kostal_idm.ini /app/kostal_idm.ini
COPY batterytimer.py /app/batterytimer.py
COPY batterytimer.ini /app/batterytimer.ini
COPY container_cron /etc/cron.d/container_cron

# set workdir
WORKDIR /app

# give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/container_cron

# apply cron job
RUN crontab /etc/cron.d/container_cron

# run the command on container startup
CMD ["cron", "-f"]
