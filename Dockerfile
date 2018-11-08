FROM debian:stretch

RUN apt-get update && apt-get install -y curl python3-dev python3-pip

# Copy project inside container
COPY . /root/app
WORKDIR /root/app

RUN /usr/bin/pip3 install -r requirements.txt

EXPOSE 5000 6667

CMD ["/usr/bin/python3", "run.py"]