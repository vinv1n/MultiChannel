#!/usr/bin/sh

# init irc bot module
git submodule init && git submodule update

# update everything
git submodule foreach git pull origin master

if [ $# -eq 0 ] then
    make all

else
    make deamon
fi