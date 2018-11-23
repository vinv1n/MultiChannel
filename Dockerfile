FROM debian:stretch

RUN apt-get update && apt-get install -y python3-dev python3-pip

# Copy project inside container
COPY . /root/api
WORKDIR /root/api

RUN /usr/bin/pip3 install -r requirements.txt

EXPOSE 5000 6667

CMD ["/usr/bin/python3", "run.py"]