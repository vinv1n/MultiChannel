FROM debian:stretch

RUN apt-get update && apt-get install -y python3-dev python3-pip cron \
    openssl

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV LC_CTYPE="en_US.UTF-8"
ENV LC_ALL=en_US.UTF-8

# Copy project inside container
COPY . /root/api
WORKDIR /root/api

RUN /usr/bin/pip3 install -r requirements.txt
RUN openssl req -batch -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

EXPOSE 5000 6667

ADD ./cron/crontab /etc/cron.d/cron-update
RUN chmod 0644 /etc/cron.d/cron-update

# mods might need to be changed
RUN chmod a+rwx /root/api/cron/update.sh

RUN cron

ENTRYPOINT ["/usr/bin/python3"]

CMD ["run.py"]