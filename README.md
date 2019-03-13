# MultiChannel
   **To update Irc submodule use:** `git submodule init && git submodule update`
# Dependencies
    Docker
    MultiChannel-IRC-bot
 
 # How to:
  ## Docker
   ### 1. **clone project**
   ### 2. **Install docker and docker-compose** https://www.docker.com/get-started
   ### 3. **go to project root**
   ### 4. run on linux `sudo docker-compose build or make all`
   ### 5. run `docker-compose up`
   ### 6. ???
   ### 7. Profit
   ### 8. -> http://0.0.0.0:5000 or http://127.0.0.1:5000
  
  ## Local
   ### Install python virtualenv
   ### Create environment `virtualenv -p python3 <env_name>`
   ### activate env `source <env_name>/bin/activate`
   ### install requirements `pip install -r requirements.txt`
   ### run project `python run.py` on project root

  ## Set up channel config
  To set up channel config, edit the config.json file on the root folder of the project.
  
  ### Email
Set the correct SMTP, SMTP port, IMAP, IMAP port, address and password of your email service provider. Please, create a new email account for this program, because the password has to be written into the config file. This might not work with all email providers. Some of the might consider the emails as spam. Gmail is not known to work. Outlook works with the system, but you should remember to verify your account so that Outlook lets you send more than a couple emails.

  ### Telegram
To set up telegram, create a new bot (https://core.telegram.org/bots) and add the token into config.json. The users should say hello to this bot, so that it can communicate with the user.

As of now, shutting down the MultiChannel App will reset the bot's memory in such a way, that it won't be able to forward user responses to the database. However, all new messages sent after the reset should work.
  ### IRC
  To configure IRC channel make sure that you have initialized and updated the IRC submodule. Next go to the config.json inside IRC-bot submodule and setup irc server, bots name and default channels.
  
  To respond theirc messages use !response <message_id> message command. You get message id once you receive message otherwise response is not registered.
  
  ## Security keys
  
  In instance/config.py, put your own secret keys in place of the placeholders.
