FROM debian:stretch

RUN apt-get update && apt-get install -y python3-dev python3-pip cron

# Copy project inside container
COPY . /root/api
WORKDIR /root/api

RUN /usr/bin/pip3 install -r requirements.txt

EXPOSE 5000 6667

ADD ./cron/crontab /etc/cron.d/cron-update
RUN chmod 0644 /etc/cron.d/cron-update
# mods might need to be changed
RUN chmod a+rwx /root/api/update.sh

RUN cron

ENTRYPOINT ["/usr/bin/python3"]

CMD ["run.py"]