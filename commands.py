import strings
from variables import *  # internal library with the environment variables
import owncloud
# library to make requests to OwnCloud server, more details on
#  https://github.com/owncloud/pyocclient
import datetime  # library to handle time
from datetime import timedelta
import operator  # library to handle dictionary
import json  # library for evaluation of json file

oc = owncloud.Client(OC_URL)  # connect to OwnCloud server
oc.login(OC_USER, OC_PWD)  # login with username and password


def name_ext(username):
    """ function created by @Hyd3L, complete code at
        https://github.com/WEEE-Open/weeelab
        Return <Name Surname> from <name.surname> string
    """
    # Extract the name and capitalize it
    first_name = username.split('.')[0].capitalize()
    # Extract the surname and capitalize it
    last_name = username.split('.')[1].capitalize()
    # Return a string of type "Name Surname"
    return first_name + " " + last_name


def start():
    """ Command "/start", Start info
    """
    return strings.msg_start


def help(user):
    """ Command "/help", Show an help.
    """
    if user.level == 1:
        return strings.msg_help_1
    else:
        return strings.msg_help


def inlab():
    """ Command "/inlab", Show the number and the name of
        people in lab.
    """
    user_inlab_list = ''
    log_file = oc.get_file_contents(LOG_PATH)
    log_lines = log_file.splitlines()
    people_inlab = log_file.count('INLAB')
    lines_inlab = [i for i, lines in enumerate(log_lines) if 'INLAB' in lines]
    # store the data of the last update of the log file,
    # the data is in UTC so we add 2 for eu/it local time
    user_file = json.loads(oc.get_file_contents(USER_PATH))
    for index in lines_inlab:
        user_inlab = log_lines[index][47:log_lines[index].rfind('>')]
        # extract the name of the person
        for user in user_file["users"]:
            user_complete_name = (user['name'] + '.' + user['surname']).lower()
            if (user_inlab == user_complete_name and (
                            user["level"] == 1 or user["level"] == 2)):
                user_inlab_list = user_inlab_list + '\n' + '- *' + name_ext(
                    user_inlab) + '*'
            elif user_inlab == user_complete_name:
                user_inlab_list = user_inlab_list + '\n' + '- ' + name_ext(
                    user_inlab)
    if people_inlab == 0:
        # Check if there aren't people in lab
        # Send a message to the user that makes
        # the request /inlab
        return 'Nobody is in lab right now.'
    elif people_inlab == 1:
        return "There is a student in lab right now:\n{}".format(
            user_inlab_list)
    else:
        return "There are {} students in lab right now:\n{}".format(
            people_inlab, user_inlab_list)


def log(command):
    """ Command "/log", Show the complete LOG_PATH file
        (only for admin user, by default only 5 lines)
        Command "/log [number]", Show the [number] most recent
        lines of LOG_PATH file
        Command "/log all", Show all lines of LOG_PATH file.
    """
    lines_message = 0  # number of lines of the message
    log_data = ''
    log_print = ''
    # Check if the message is the command /
    log_file = oc.get_file_contents(LOG_PATH)
    log_lines = log_file.splitlines()
    lines_to_print = len(log_lines)
    if len(command) > 1 and command[1].isdigit() and lines_to_print > int(
            command[1]):
        # check if the command is "/log [number]"
        lines_to_print = int(command[1])
    for lines_printed in reversed(range(0, lines_to_print)):
        if not ("INLAB" in log_lines[lines_printed]):
            if log_data == log_lines[lines_printed][1:11]:
                log_line_to_print = '_' + log_lines[lines_printed][
                                          47:log_lines[lines_printed].rfind(
                                              ">")] + '_' + log_lines[
                                                                lines_printed][
                                                            log_lines[
                                                                lines_printed].rfind(
                                                                ">") + 1:len(
                                                                log_lines[
                                                                    lines_printed])]
                log_print = log_print + '{}\n'.format(log_line_to_print)
                lines_message += 1
            else:
                if len(command) == 1 and lines_message > 0:
                    ines_printed = len(log_lines)
                else:
                    log_data = log_lines[lines_printed][1:11]
                    log_line_to_print = '\n*' + log_data + '*\n_' + \
                                        log_lines[lines_printed][
                                        47:log_lines[
                                            lines_printed].rfind(
                                            ">")] + '_' + log_lines[
                                                              lines_printed][
                                                          log_lines[
                                                              lines_printed].rfind(
                                                              ">") + 1:len(
                                                              log_lines[
                                                                  lines_printed])]
                    log_print = log_print + '{}\n'.format(
                        log_line_to_print)
                    lines_message += 1
        if lines_message > 25:
            log_print = log_print.replace('[', '\[')
            log_print = log_print.replace('::', ':')
            return '{}\n'.format(log_print)
    log_print = log_print.replace('[', '\[')
    log_print = log_print.replace('::', ':')
    log_update_data = oc.file_info(LOG_PATH).get_last_modified() + timedelta(
        hours=2)
    return '{}\nLatest log update: *{}*'.format(log_print, log_update_data)


def stat(command, user):
    """ Command "/stat name.surname",
        Show hours spent in lab by name.surname user.
    """
    user_hours = 0  # initialize hour variable, type int
    user_minutes = 0  # initialize minute variable, type int
    hours_sum = datetime.timedelta(hours=user_hours, minutes=user_minutes)
    found_user = False
    # create a control variable used
    # to check if name.surname is found
    if len(command) == 1:
        user_name = user["name"].lower() + '.' + user["surname"].lower()
        # print user_name
    elif (len(command) != 1) and (user['level'] == 1):
        # Check if the command has option or not
        user_name = str(command[1])
        # store the option in a variable
    else:
        return "Sorry! You are not allowed to see stat of other users!\n" \
               "Only admin can!"

    log_file = oc.get_file_contents(LOG_PATH)
    log_lines = log_file.splitlines()
    for lines in log_lines:
        if not ("INLAB" in lines) and (
                    user_name == lines[47:lines.rfind(">")]):
            found_user = True
            # extract the hours and minute
            # from char 39 until ], splitted by :
            (user_hours, user_minutes) = lines[39:lines.rfind("]")].split(':')
            # convert hours and minutes in datetime
            partial_hours = datetime.timedelta(hours=int(user_hours),
                                               minutes=int(user_minutes))
            hours_sum += partial_hours
            # sum to the previous hours
    if not found_user:
        return "No statistics for the given user. " \
               "Have you typed it correctly? (name.surname)"
    else:
        total_second = hours_sum.total_seconds()
        total_hours = int(total_second // 3600)
        total_minutes = int(
            (total_second % 3600) // 60)
        log_update_data = oc.file_info(
            LOG_PATH).get_last_modified() + timedelta(hours=2)
        return 'Stat for the user {}\nHH:MM = {:02d}:{:02d}\n\n' \
               'Latest log update:\n*{}*'.format(
            name_ext(user_name), total_hours, total_minutes, log_update_data)
        # write the stat of the user


def top(command, user):
    """ Command "/top",
        Show a list of the top users in lab (defaul top 50).
    """
    # Check if the message is the command /top
    users_name = []
    users_hours = {}
    top_list_print = 'Top User List!\n'
    position = 0
    number_top_list = 100
    today = datetime.date.today()
    month = today.month
    year = today.year
    if user['level'] == 1:
        if len(command) == 1:
            month_log = month
            year_log = year
        elif command[1] == "all":
            month_log = 4
            year_log = 2017
        for log_datayear in range(year_log, year + 1):
            for log_datamonth in range(month_log, month + 1):
                try:
                    if log_datamonth == month and log_datayear == year:
                        log_file = oc.get_file_contents(LOG_PATH)
                        # log_file = open(LOG_PATH).read()
                        log_lines = log_file.splitlines()
                    else:
                        if log_datamonth < 10:
                            datamonth = "0" + str(log_datamonth)
                        else:
                            datamonth = str(log_datamonth)
                        log_file = oc.get_file_contents(
                            LOG_BASE + "log" + str(
                                log_datayear) + datamonth + ".txt")
                        # log_file = open(LOG_BASE + "log" + str(log_datayear) + datamonth + ".txt")
                        log_lines = log_file.splitlines()
                    for lines in log_lines:
                        if not ("INLAB" in lines):
                            name = lines[47:lines.rfind(">")].encode(
                                'utf-8')
                            (user_hours, user_minutes) = lines[
                                                         39:lines.rfind(
                                                             "]")].split(
                                ':')
                            partial_hours = datetime.timedelta(
                                hours=int(user_hours),
                                minutes=int(user_minutes))
                            if name in users_name:
                                # check if user was already found
                                users_hours[name] += partial_hours
                                # add to the key with the same name
                                # the value partial_hours
                            else:
                                users_name.append(name)
                                # create a new key with the name
                                users_hours[name] = partial_hours
                                # add the hours to the key
                except owncloud.owncloud.HTTPResponseError:
                    print("Error open file.")
        # sort the dict by value in descendet order
        sorted_top_list = sorted(users_hours.items(),
                                 key=operator.itemgetter(1), reverse=True)
        # print sorted_top_list
        for rival in sorted_top_list:
            # print the elements sorted
            if position < number_top_list:
                # check if the list is completed
                # extract the hours and minutes from dict,
                # splitted by :
                total_second = rival[1].total_seconds()
                total_hours = int(total_second // 3600)
                total_minutes = int((total_second % 3600) // 60)
                # add the user to the top list
                user_file = json.loads(oc.get_file_contents(USER_PATH))
                for user in user_file["users"]:
                    user_complete_name = user["name"].lower() + '.' + user[
                        "surname"].lower()
                    if rival[0] == user_complete_name:
                        position += 1
                        # update the counter of position on top list
                        if user["level"] == 1 or user["level"] == 2:
                            top_list_print = top_list_print + '{}) \[{:02d}:{:02d}] *{}*\n'.format(
                                position, total_hours, total_minutes,
                                name_ext(rival[0]))
                        else:
                            top_list_print = top_list_print + '{}) \[{:02d}:{:02d}] {}\n'.format(
                                position, total_hours, total_minutes,
                                name_ext(rival[0]))
        log_update_data = oc.file_info(
            LOG_PATH).get_last_modified() + timedelta(hours=2)
        return '{}\nLatest log update: \n*{}*'.format(top_list_print,
                                                      log_update_data)
        # send the top list to the user
    else:
        return 'Sorry! You are not allowed to use this function! \n' \
               'Only admin can use!'


def save_id(user_id, user_name):
    user_bot_contents = oc.get_file_contents(USER_BOT_PATH)
    # user_bot_contents = open(USER_BOT_PATH)
    # read the content of the user file stored in owncloud server
    if user_id in user_bot_contents:
        # Check if the user is already recorded
        pass
    else:
        # Store a new user name and id in a file on owncloud server,
        # encoding in utf.8
        try:
            user_bot_contents = user_bot_contents.decode('utf-8') \
                                + '\'' + user_name.encode('utf-8') \
                                + '\'' + ': ' + '\'' + str(user_id) \
                                + '\'' + ', '
            oc.put_file_contents(USER_BOT_PATH,
                                 user_bot_contents.encode('utf-8'))
            # user_file.write(user_bot_contents.encode('utf-8'))
            # write on the file the new data
        except AttributeError:
            pass
