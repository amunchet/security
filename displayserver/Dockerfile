#  Created by Marcello Monachesi at 9/6/19, 5:39 PM
FROM centos:7

# default arguments
ARG USER_ID=1000
ARG GROUP_ID=1000
ARG FTP_USER=admin
ARG FTP_PASSWORD=pass
ARG TIMEZONE=Europe/Berlin

RUN useradd -m -r -u ${USER_ID} appuser

RUN groupmod -g ${GROUP_ID} appuser

WORKDIR /home/appuser

# install python 3
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum update
RUN yum install -y python36u python36u-libs python36u-devel python36u-pip

# install cron
RUN yum install -y cronie
RUN sed -i -e '/pam_loginuid.so/s/^/#/' /etc/pam.d/crond

# set timezone
RUN unlink /etc/localtime
RUN ln -s /usr/share/zoneinfo/${TIMEZONE} /etc/localtime

# install requirements
COPY requirements.txt ./
RUN python3.6 -m venv venv
RUN venv/bin/pip install -r requirements.txt

# copy app files into container
COPY app app
COPY migrations migrations
COPY displayserverbackend.py config.py boot.sh filemanagement.py ./

# grant owner permission to appuser
RUN chown -R appuser:appuser /home/appuser

# config cron for the user appuser
USER appuser
RUN chmod +x filemanagement.py
# run backup every 10 minutes
RUN echo -e "*/10 * * * * source /home/appuser/venv/bin/activate && source /home/appuser/dbenv && python3.6 /home/appuser/filemanagement.py -d \"/home/appuser/data/${FTP_USER}\" >> /tmp/backup.log 2>&1 \n" > mycron
# create mising folders every minute
RUN echo -e "* * * * * source /home/appuser/venv/bin/activate && source /home/appuser/dbenv && python3.6 /home/appuser/filemanagement.py -c -d \"/home/appuser/data/${FTP_USER}\" >> /tmp/backup.log 2>&1 \n" >> mycron
RUN crontab mycron
RUN rm mycron

# swhich to root user
USER root
RUN chmod +x boot.sh

# set env variables
ENV FLASK_APP displayserverbackend.py
ENV FTP_USER=${FTP_USER}
ENV FTP_PASSWORD=${FTP_PASSWORD}

ENTRYPOINT ["./boot.sh"]
