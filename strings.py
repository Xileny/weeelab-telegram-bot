level_0 = "Sorry! You are not allowed to use this bot\n" \
          "Please contact us [mail](weeeopen@polito.it), visit our " \
          "[WeeeOpen FB page](https://www.facebook.com/weeeopenpolito/) and " \
          "the site [WeeeOpen](http://weeeopen.polito.it/) for more info.\n" \
          "After authorization /start the bot."
error_command = "Error, command not found"

msg_start = "*WEEE-Open Telegram bot*.\n" \
            "The goal of this bot is to obtain information about who is " \
            "currently in the lab, who has done what, compute some stats " \
            "and, in general, simplify the life of our members and " \
            "to avoid waste of paper as well. \nAll data is read from " \
            "a weeelab log file, which is fetched from an OwnCloud " \
            "shared folder. \nFor a list of the commands allowed send /help."

msg_help = "Available commands and options:\n\n" \
           "/inlab - Show the people in lab\n" \
           "/log - Show last 5 login\n" \
           "  + _number_ - Show last _number_ login\n" \
           "  + _all_ - Show all login\n" \
           "/stat - Show hours spent in lab by the user\n"

msg_help_1 = msg_help + \
             "\n*only for admin user*\n" \
             "/stat _name.surname_ - Show hours spent in lab by this user\n" \
             "/top - Show a list of top users in lab\n"
