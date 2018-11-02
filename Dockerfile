FROM debian:stretch

RUN apt-get update && apt-get install -y curl python3-dev python3-pip gnupg build-essential

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
RUN echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/4.0 main" | tee /etc/apt/sources.list.d/mongodb-org-4.0.list

# install mongodb
RUN apt-get update &&  apt-get install -y mongodb-org

# Copy project inside container
COPY . /root/app
WORKDIR /root/app

RUN /usr/bin/pip3 install -r requirements.txt

EXPOSE 5000 6667

CMD ["/usr/bin/python3", "run.py"]