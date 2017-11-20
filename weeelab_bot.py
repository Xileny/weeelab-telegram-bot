#!/usr/bin/env python
# coding:utf-8

"""
WEEELAB_BOT - Telegram bot.
Author: WeeeOpen Team
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
NOTE: The print commands are only for debug.
"""

# Modules
import json

import telepot
from telepot.loop import MessageLoop

import commands
import strings
from variables import *  # internal library with the environment variables


# call when a new message arrive
def on_chat_message(msg):
    user_id = msg['from']['id']  # User Telegram ID
    user_name = msg['from']['first_name']  # name of the  Telegram user
    # user_username = msg['from']['username']  # username of the  Telegram user
    chat_id = msg['chat']['id']  # chat Telegram ID between user and bot
    chat_type = msg['chat']['type']  # type of Telegram chat
    command = msg['text'].split()  # array of the words of the Telegram message

    user_file = json.loads(commands.oc.get_file_contents(USER_PATH))

    level = 0
    user = ''
    for u in user_file['users']:
        if u['telegramID'] == user_id:
            level = u['level']
            user = u

    if chat_type == 'private':
        if level == 0:
            bot.sendMessage(chat_id, strings.level_0, 'Markdown')
            commands.save_id(user_id, user_name)
        else:
            if command[0] == '/start':
                message = commands.start()
                bot.sendMessage(chat_id, message, 'Markdown')
            elif command[0] == '/help':
                message = commands.help(user)
                bot.sendMessage(chat_id, message, 'Markdown')
            elif command[0] == '/inlab':
                message = commands.inlab()
                bot.sendMessage(chat_id, message, 'Markdown')
            elif command[0] == '/log':
                message = commands.log(command)
                bot.sendMessage(chat_id, message, 'Markdown')
            elif command[0] == '/stat':
                message = commands.stat(command, user)
                bot.sendMessage(chat_id, message, 'Markdown')
            elif command[0] == '/top':
                message = commands.top(command, user)
                bot.sendMessage(chat_id, message, 'Markdown')
            else:
                # bot.sendMessage(chat_id, strings.error_command, 'Markdown')
                print(strings.error_command)
    else:
        pass


if __name__ == '__main__':
    try:
        # get the token
        with open("TOKEN") as file:
            TOKEN = file.read()

        bot = telepot.Bot(TOKEN)  # init the bot
        # call when an update arrive
        MessageLoop(bot, {'chat': on_chat_message}).run_as_thread()

        print('The bot was started at...')  # TODO add the start time

    # run the bot until a keyboard interrupt is called
    except KeyboardInterrupt:
        exit()
