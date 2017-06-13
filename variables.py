import os # system library needed to read the environment variables

# get environment variables
OC_URL = os.environ.get('OC_URL')  # url of the OwnCloud server
OC_USER = os.environ.get('OC_USER')  # OwnCloud username
OC_PWD = os.environ.get('OC_PWD')  # OwnCloud password
# path of the file with authorized users in OwnCloud (/folder/file.json)
USER_PATH = os.environ.get('USER_PATH')
# path of the log file to read in OwnCloud (/folder/file.txt)
LOG_PATH = os.environ.get('LOG_PATH')
# path of the file to store bot users in OwnCloud (/folder/file.txt)
USER_BOT_PATH = os.environ.get('USER_BOT_PATH')
TOKEN_BOT = os.environ.get('TOKEN_BOT')  # Telegram token for the bot API