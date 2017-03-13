

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import html
import requests
import configparser
import urllib
from urllib.request import urlopen
from urllib.parse import quote_plus
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler
from telegram import InlineQueryResultArticle, ChatAction, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Chat, User, Message, Update, ChatMember, UserProfilePhotos, File, ReplyMarkup, TelegramObject
from uuid import uuid4
import subprocess
import time
import logging
import json
from json import JSONDecoder
from functools import partial

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
def __repr__(self):
    return str(self)

config = configparser.ConfigParser()
config.read('bot.ini')

TOKEN = config['KEYS']['bot_api']
PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(TOKEN)

jenkins = config['JENKINS']['url']
user = config['JENKINS']['user']
password = config['JENKINS']['password']
token = config['JENKINS']['token']
job = config['JENKINS']['job']
gerrituser = config['GERRIT']['user']
gerriturl = config['GERRIT']['url']
protocol = config['GERRIT']['protocol']
jenkinsconfig = config['JENKINS']['on']
username = config['ADMIN']['username']
dispatcher = updater.dispatcher


hereyago = "Here's a list of commands for you to use:\n"
build_help = "/build to start the build process\n"
changelog_help = "/changelog 'text' to set the changelog\n"
sync_help = "/sync to set sync to on/off\n"
clean_help = "/clean to set clean to on/off\n"
repopick_a_help = "/repopick to set repopick on or off\n"
reset_help = "/reset to set reset on or off\n"
repopick_b_help = "-- /repopick `changes` to pick from gerrit on build\n"
open_a_help = "/open to see all open changes\n"
open_b_help = "-- /open `projects` to see open changes for certain projects\n"
pickopen_help = "/pickopen to pick all open changes on gerrit\n"
help_help = "/help to see this message\n--/help 'command' to see information about that command :)" # love this lmao help_help

jenkinsnotmaster = "Sup *not* master. \n" + hereyago + open_a_help + open_b_help + help_help
nojenkinsnotmaster = "Sup *not* master. \n" + hereyago + open_a_help + open_b_help + help_help
jenkinsmaster = "Sup" + username + "\n" + hereyago + build_help + changelog_help + sync_help + clean_help + repopick_a_help + reset_help + repopick_b_help + pickopen_help + open_a_help + open_b_help + help_help
nojenkinsmaster = "Sup" + username + "\n" + hereyago + open_a_help + open_b_help + help_help


cg = "This is an automated build, provided by @BruhhJenkinsBot."
cg = quote_plus(cg)
syncparam = "true"
cleanparam = "false"
repopickstatus = "false"
rpick = ""  
reporeset = "false"
release = "false"
def get_admin_ids(bot, chat_id):
    """Returns a list of admin IDs for a given chat."""
    return [admin.user.id for admin in bot.getChatAdministrators(chat_id)]

def start(bot, update):
    if update.message.chat.type == "private":

        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.TYPING)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Hi. I'm Hunter's Jenkins Bot! You can use me to do lots of cool stuff, assuming your name is @hunter_bruhh! If not, then I'm not much use to you right now! Maybe he'll implement some cool stuff later!")
        if update.message.from_user.id != int(config['ADMIN']['id']):
            if jenkinsconfig == "yes":
                bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)
                time.sleep(1)
                bot.sendMessage(chat_id=update.message.chat_id,
                                text=jenkinsnotmaster)
                bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)
            else:
                bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)
                time.sleep(1)
                bot.sendMessage(chat_id=update.message.chat_id,
                                text=nojenkinsnotmaster)
                bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)
        else:
            if jenkinsconfig == "yes":
                bot.sendMessage(chat_id=update.message.chat_id,
                                text=jenkinsmaster)
                bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)
            else:
                bot.sendMessage(chat_id=update.message.chat_id,
                                text=nojenkinsmaster)
                bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)

def help_message(bot, update, args):
    jenkinsmasterlist = ["build", "changelog", "sync", "clean", "repopick", "pickopen", "open"]
    nojenkinsmasterlist = ["open"]
    nojenkinslist = ["open"]
    jenkinslist = ["open"]
    args_length = len(args)
    if update.message.from_user.id != int(config['ADMIN']['id']):
        if jenkinsconfig == "yes":
            if args_length != 0:
                if args_length > 1:
                    for x in jenkinslist:
                        try:
                            helpme
                        except NameError:
                            helpmeplox = "Please use only one argument. A list of arguments aka commands to ask about would be:\n"
                    helpmeplox = helpmeplox + x + ",\n"
                    helpme = helpmeplox
                else:
                    if args[0] in jenkinslist:
                        if args[0] == "open":
                            helpme = open_a_help + open_b_help
                    else:
                        helpme = "That's not a command to ask about."
                bot.sendChatAction(chat_id=update.message.chat_id,
                               action=ChatAction.TYPING)
                time.sleep(1)
                bot.sendMessage(chat_id=update.message.chat_id,
                                text=helpme)
            else:
                bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)
                time.sleep(1)
                bot.sendMessage(chat_id=update.message.chat_id,
                                text=jenkinsnotmaster)
        else:
            if args_length != 0:
                if args_length > 1:
                    for x in nojenkinslist:
                        try:
                            helpme
                        except NameError:
                            helpmeplox = "Please use only one argument. A list of arguments aka commands to ask about would be:\n"
                    helpmeplox = helpmeplox + x + ",\n"
                    helpme = helpmeplox
                else:
                    if args[0] in nojenkinslist:
                        if args[0] == "open":
                            helpme = open_a_help + open_b_help
                    else:
                        helpme = "That's not a command to ask about."
                bot.sendChatAction(chat_id=update.message.chat_id,
                               action=ChatAction.TYPING)
                time.sleep(1)
                bot.sendMessage(chat_id=update.message.chat_id,
                                text=helpme)
                bot.sendChatAction(chat_id=update.message.chat_id,
                               action=ChatAction.TYPING)
                time.sleep(1)
                bot.sendMessage(chat_id=update.message.chat_id,
                                text=helpme)
            else:
                bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)
                time.sleep(1)
                bot.sendMessage(chat_id=update.message.chat_id,
                                text=nojenkinsnotmaster)
    else:
        if jenkinsconfig == "yes":
            if args_length != 0:
                if args_length > 1:
                    for x in jenkinsmasterlist:
                        try:
                            helpme
                        except NameError:
                            helpmeplox = "Please use only one argument. A list of arguments aka commands to ask about would be:\n"
                    helpmeplox = helpmeplox + x + ",\n"
                    helpme = helpmeplox
                else:
                    if args[0] in jenkinsmasterlist:
                        if args[0] == "build":
                            helpme = build_help
                        if args[0] == "changelog":
                            helpme = changelog_help
                        if args[0] == "sync":
                            helpme = sync_help
                        if args[0] == "clean":
                            helpme = clean_help
                        if args[0] == "repopick":
                            helpme = repopick_a_help + repopick_b_help
                        if args[0] == "pickopen":
                            helpme = pickopen_help
                        if args[0] == "open":
                            helpme = open_a_help + open_b_help
                    else:
                        helpme = "That's not a command to ask about."
                bot.sendChatAction(chat_id=update.message.chat_id,
                               action=ChatAction.TYPING)
                time.sleep(1)
                bot.sendMessage(chat_id=update.message.chat_id,
                                text=helpme)
            else:
                bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)
                time.sleep(1)
                bot.sendMessage(chat_id=update.message.chat_id,
                                text=jenkinsmaster)
        else:
            if args_length != 0:
                if args_length > 1:
                    for x in nojenkinsmasterlist:
                        try:
                            helpme
                        except NameError:
                            helpmeplox = "Please use only one argument. A list of arguments aka commands to ask about would be:\n"
                    helpmeplox = helpmeplox + x + ",\n"
                    helpme = helpmeplox
                else:
                    if args[0] in nojenkinsmasterlist:
                        if args[0] == "build":
                            helpme = build_help
                        if args[0] == "changelog":
                            helpme = changelog_help
                        if args[0] == "sync":
                            helpme = sync_help
                        if args[0] == "clean":
                            helpme = clean_help
                        if args[0] == "repopick":
                            helpme = repopick_a_help + repopick_b_help
                        if args[0] == "pickopen":
                            helpme = pickopen_help
                        if args[0] == "open":
                            helpme = open_a_help + open_b_help
                    else:
                        helpme = "That's not a command to ask about."
                bot.sendChatAction(chat_id=update.message.chat_id,
                               action=ChatAction.TYPING)
                time.sleep(1)
                bot.sendMessage(chat_id=update.message.chat_id,
                                text=helpme)
            else:
                bot.sendChatAction(chat_id=update.message.chat_id,
                                   action=ChatAction.TYPING)
                time.sleep(1)
                bot.sendMessage(chat_id=update.message.chat_id,
                                text=nojenkinsmaster)

def link(bot, update, args):
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.TYPING)
        str_args = ' '.join(args)
        args_length = len(args)
        if str_args == "":
                bot.sendMessage(chat_id=update.message.chat_id,
                                text="You must provide change numbers to get a link to each change\n e.g. /link 99 123 345",
                                parse_mode="Markdown")
        else:
            for i in range(args_length):
                try:
                    link
                except NameError:
                    link = ""
                link = link + args[i] + " - " + protocol + "://" + gerriturl + "/#/c/" + args[i] + "/" + "\n"
            bot.sendMessage(chat_id=update.message.chat_id,
                                text=link)


def openchanges(bot, update, args):

        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.TYPING)
        curl = "rm open.json && curl -H 'Accept-Type: application/json' " + protocol + "://" + gerrituser + "@" + gerriturl + "/changes/?q=status:open | sed '1d' > open.json"
        command = subprocess.Popen(curl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
        with open('open.json', encoding='utf-8') as data_file:
            data = json.load(data_file)
        dict_length = len(data)
        str_args = ' '.join(args)
        args_length = len(args)
        if str_args != "":
            for i in range(dict_length):
                try:
                    openc
                except NameError:
                    openc = ""
                if str(data[i]['project']) in args:
                    openc = openc + "\n" + "<a href=" + '"' + protocol + "://" + gerriturl + "/#/c/" + str(data[i]['_number']) + "/" + '"' + ">" + html.escape(str(data[i]['_number'])) + "</a>" + html.escape(" - " + str(data[i]['subject']))
            print(openc)
            for i in range(dict_length):
                try:
                    cnum
                except NameError:
                    cnum = "/repopick"
                if str(data[i]['project']) in args:
                    cnum = cnum + " " + str(data[i]['_number'])
        else:
            for i in range(dict_length):
                try:
                    openc
                except NameError:
                    openc = ""
                openc = openc + "\n" + "<a href=" + '"' + protocol + "://" + gerriturl + "/#/c/" + str(data[i]['_number']) + "/" + '"' + ">" + html.escape(str(data[i]['_number'])) + "</a>" + html.escape(" - " + str(data[i]['subject']))
            for i in range(dict_length):
                try:
                    cnum
                except NameError:
                    cnum = "/repopick"
                cnum = cnum + " " + str(data[i]['_number'])
        print(openc)
        print(cnum)
        if update.message.from_user.id == int(config['ADMIN']['id']) and update.message.chat.type == "private":

            bot.sendMessage(chat_id=update.message.chat_id,
                            text=openc,
                            parse_mode="HTML")
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=cnum,
                            parse_mode="Markdown")
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=openc,
                            parse_mode="HTML")

if jenkinsconfig == "yes":
    def pickopen(bot, update):
        if update.message.from_user.id == int(config['ADMIN']['id']):
            bot.sendChatAction(chat_id=update.message.chat_id,
                               action=ChatAction.TYPING)
            curl = "rm open.json && curl -H 'Accept-Type: application/json' " + protocol + "://" + gerrituser + "@" + gerriturl + "/changes/?q=status:open | sed '1d' > open.json"
            command = subprocess.Popen(curl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            with open('open.json', encoding='utf-8') as data_file:
                data = json.load(data_file)
            dict_length = len(data)
            for i in range(dict_length):
                try:
                    cnumbers
                except NameError:
                    cnumbers = ""
                cnumbers = cnumbers + " " + str(data[i]['_number'])
            print(cnumbers)
            text = "I will pick all open changes: " + cnumbers
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=text,
                            parse_mode="Markdown")
            global rpick
            cnumbers.replace(" ", "%20")
            cnumbers_url = cnumbers.replace(" ", "%20")
            rpick = cnumbers_url

def choosebuild(bot, update):
    if update.message.from_user.id == int(config['ADMIN']['id']):
        keyboard = [[InlineKeyboardButton("Without Paramaters", callback_data='build')],

                    [InlineKeyboardButton("With Parameters", callback_data='buildWithParameters')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please choose a build style:', reply_markup=reply_markup)

def sync(bot, update):
    if update.message.from_user.id == int(config['ADMIN']['id']):
        keyboard = [[InlineKeyboardButton("YES", callback_data='syncon')],

                    [InlineKeyboardButton("NO", callback_data='syncoff')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Would you like to sync on a new build?:', reply_markup=reply_markup)

def reset(bot, update):
    if update.message.from_user.id == int(config['ADMIN']['id']):
        keyboard = [[InlineKeyboardButton("YES", callback_data='reseton')],

                    [InlineKeyboardButton("NO", callback_data='resetoff')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Would you like to reporeset?:', reply_markup=reply_markup)


def clean(bot, update):
    if update.message.from_user.id == int(config['ADMIN']['id']):
        keyboard = [[InlineKeyboardButton("YES", callback_data='cleanon')],

                    [InlineKeyboardButton("NO", callback_data='cleanoff')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Would you like to clean on a new build?:', reply_markup=reply_markup)

def setrelease(bot, update):
    if update.message.from_user.id == int(config['ADMIN']['id']):
        keyboard = [[InlineKeyboardButton("YES", callback_data='releaseon')],

                    [InlineKeyboardButton("NO", callback_data='releaseoff')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Would you like to do a release?', reply_markup=reply_markup)


def buildwithparams(bot, update, query):
    query = update.callback_query
    bot.sendMessage(chat_id=query.message.chat_id,
                    text="You have selected the 'buildWithParameters option, this will include a custom changelog with your build, and will specify whether to sync & clean or not",
                    parse_mode="Markdown")
    user_id = update.callback_query.from_user.id
    command_string = jenkins + "/job/" + job + "/buildWithParameters?token=" + token + "&changelog=" + cg + "&SYNC=" + syncparam + "&CLEAN=" + cleanparam + "&repopicks=" + rpick + "&REPORESET=" + reporeset + "&RELEASE=" + release
    command = "curl --user " + user + ":" + password + " " + "'" + command_string + "'"
    print (command)
    if user_id == int(config['ADMIN']['id']):
        bot.sendChatAction(chat_id=query.message.chat_id,
                                       action=ChatAction.TYPING)
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = output.stdout.read().decode('utf-8')
        output = '`{0}`'.format(output)

        bot.sendMessage(chat_id=query.message.chat_id,
                                    text=output,
                                    parse_mode="Markdown")

def buildwithoutparams(bot, update, query):
    user_id = update.callback_query.from_user.id
    command_string = jenkins + "/job/" + job + "/buildWithParameters?token=" + token
    command = "curl --user " + user + ":" + password + " " + "'" + command_string + "'"
    print (command)
    if user_id == int(config['ADMIN']['id']):
        bot.sendChatAction(chat_id=query.message.chat_id,
                           action=ChatAction.TYPING)
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = output.stdout.read().decode('utf-8')
        output = '`{0}`'.format(output)

        bot.sendMessage(chat_id=query.message.chat_id,
                        text=output, parse_mode="Markdown")

def changelog(bot, update, args):
        if update.message.from_user.id == int(config['ADMIN']['id']):
            global cg
            user = update.message.from_user

            str_args = ' '.join(args)
            if str_args != "":
                update.message.reply_text('Changelog updated: ' + "'" + str_args + "'")
                cgs = '%20'.join(args)
                cg = cgs
                print ("Changelog set to " + "'" + cg + "'")
            else:
                bot.sendMessage(chat_id=update.message.chat_id,
                                text="You cannot provide an empty changelog.",
                                parse_mode="Markdown")

def repopick(bot, update, args):
        if update.message.from_user.id == int(config['ADMIN']['id']):
            global rpick
            global repopickstatus
            user = update.message.from_user

            str_args = ' '.join(args)
            if str_args != "":
                update.message.reply_text('I will pick changes: ' + "'" + str_args + "'")
                rpicks = '%20'.join(args)
                rpick = rpicks
                repopickstatus = "true"
                print ("Repopick set to" + "'" + rpick + "'")
            else:
                keyboard = [[InlineKeyboardButton("ON", callback_data='repopickon')],

                            [InlineKeyboardButton("OFF", callback_data='repopickoff')]]

                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text('Turn repopick ON or OFF:', reply_markup=reply_markup)

def button(bot, update, direct=True):
        user_id = update.callback_query.from_user.id
        if user_id == int(config['ADMIN']['id']):
            query = update.callback_query

            selected_button = query.data
            global cleanparam
            global syncparam
            global repopickstatus
            global reporeset
            global release
            if selected_button == 'buildWithParameters':
                bot.editMessageText(text="Selected option: With Paramaters",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                buildwithparams(bot, update, query)
            if selected_button == 'build':
                bot.editMessageText(text="Selected option: Without Paramaters",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                buildwithoutparams(bot, update, query)
            if selected_button == 'syncon':
                bot.editMessageText(text="Sync set to true",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                syncparam = "true"
            if selected_button == 'syncoff':
                bot.editMessageText(text="Sync set to false",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                syncparam = "false"
            if selected_button == 'cleanon':
                bot.editMessageText(text="Clean set to true",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                cleanparam = "true"
            if selected_button == 'cleanoff':
                bot.editMessageText(text="Clean set to false",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                cleanparam = "false"
            if selected_button == 'repopickon':
                bot.editMessageText(text="Repopick set to ON",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                repopickstatus = "true"
            if selected_button == 'repopickoff':
                bot.editMessageText(text="Repopick set to OFF",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                repopickstatus = "false"
            if selected_button == 'reseton':
                bot.editMessageText(text="Reporeset set to ON",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                reporeset = "true"
            if selected_button == 'resetoff':
                bot.editMessageText(text="Reporeset set to OFF",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                reporeset = "false"
            if selected_button == 'releaseon':
                bot.editMessageText(text="Release set to ON",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                release = "true"
            if selected_button == 'releaseoff':
                bot.editMessageText(text="Release set to OFF",
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)
                release = "false"
        return False

def inlinequery(bot, update):
    query = update.inline_query.query
    o = execute(query, update, direct=False)
    results = list()

    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title=query,
                                            description=o,
                                            input_message_content=InputTextMessageContent(
                                            '*{0}*\n\n{1}'.format(query, o),
                                            parse_mode="Markdown")))

    bot.answerInlineQuery(update.inline_query.id, results=results, cache_time=10)

if jenkinsconfig == "yes":
    pickopen_handler = CommandHandler('pickopen', pickopen)
    sync_handler = CommandHandler('sync', sync)
    clean_handler = CommandHandler('clean', clean)
    release_handler = CommandHandler('release', setrelease)
    build_handler = CommandHandler('build', choosebuild)
    repopick_handler = CommandHandler('repopick', repopick, pass_args=True)
    changelog_handler = CommandHandler('changelog', changelog,  pass_args=True)
    reset_handler = CommandHandler('reset', reset)
start_handler = CommandHandler('start', start)
open_handler = CommandHandler('open', openchanges, pass_args=True)
help_handler = CommandHandler('help', help_message, pass_args=True)
link_handler = CommandHandler('link', link, pass_args=True)
if jenkinsconfig == "yes":
    dispatcher.add_handler(pickopen_handler)
    dispatcher.add_handler(sync_handler)
    dispatcher.add_handler(clean_handler)
    dispatcher.add_handler(release_handler)
    dispatcher.add_handler(build_handler)
    dispatcher.add_handler(repopick_handler)
    dispatcher.add_handler(changelog_handler)
    dispatcher.add_handler(reset_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(open_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(link_handler)
dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(InlineQueryHandler(inlinequery))
dispatcher.add_error_handler(error)

updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.setWebhook("https://bruhhreviewbot.herokuapp.com/" + TOKEN)
updater.idle()
