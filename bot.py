#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
"""

import logging
import operator

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import *
from os import environ
from sys import exit
from functools import wraps
from random import randint
from time import sleep

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

env_vars = {
    'OPS_LIST': 'OPS_LIST env var is required. Example: OPS_LIST=@ultradesu,@username2,144178090',
    'TG_TOKEN': 'TG_TOKEN env var is required. Example: TG_TOKEN=<bot_token>',
    'ALLOWED_CHAT': 'ALLOWED_CHAT env var is required. Example: ALLOWED_CHAT=<-380465766>',
}

# parse all envvars from env_vars dict
config = dict()
for envvar, message in env_vars.items():
    vars()[envvar] = environ.get(envvar, None)
    if vars()[envvar] is None:
        logger.error(message)
        exit(228)
    else:
        if 'TOKEN' in envvar:
            logger.info(f"Parsed: {envvar} = ***")
        else:
            logger.info(f"Parsed: {envvar} = {vars()[envvar]}")
        config[envvar] = vars()[envvar]

# bot instance for sending update unrelated actions.
bot = Bot(config['TG_TOKEN'])

# parse opses
opses = list()
try:
    for ops in config['OPS_LIST'].split(','):
        if ops.isdigit():
            name = bot.get_chat_member(config['ALLOWED_CHAT'], ops)['user']['first_name']
            ops=f"[{name}](tg://user?id={ops})"
        opses.append(ops)
except Exception as error:
    logger.error(f"Can't parse OPS_LIST env var: {error}")
logger.info(f"Ops list ({len(opses)}): {', '.join(opses)}")
config['OPS_LIST'] = opses

# permissions scheme. allow only ALLOWED_CHAT
def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        conf_id = update.effective_chat.id
        conf_title = update.effective_chat.title
        if str(conf_id) != str(config['ALLOWED_CHAT']):
            logger.warning("Unauthorized access denied for {} ({}).".format(
                  conf_title,
                  conf_id))
            update.message.reply_text("Unauthorized access denied for {} ({}).".format(
                  conf_title,
                  conf_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped

# help text
help_text = f"""This bot will choose your destiny.

*Configured Ops list:*

{', '.join(config['OPS_LIST'])}

*Commands:*
/roll - Roll the dice for all Ops at once.
...
"""

# handlers
@restricted
def help(update, context):
    """Send a message when the commands /start, /help is issued."""
    update.message.reply_markdown(
        text=help_text)

@restricted
def roll(update, context):
    """Send a message when the command /roll is issued."""
    result = dict()
    bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING
    )
    message_id = update.message.reply_markdown(f"_Rolling._")
    sleep(1)
    bot.edit_message_text(chat_id=update.message.chat_id,
                      parse_mode='Markdown',
                      message_id=message_id.message_id,
                      text='_Rolling.._',)
    bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING
    )
    sleep(1)
    bot.edit_message_text(chat_id=update.message.chat_id,
                      parse_mode='Markdown',
                      message_id=message_id.message_id,
                      text='_Rolling..._',)
    bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING
    )
    sleep(1)
    for ops in config['OPS_LIST']:
        result[ops] = randint(1, 100)
    result = sorted(result.items(),key=operator.itemgetter(1),reverse=False)
    body = ""
    for user, score in result:
        if user.isdigit():
            user = f"[{user}](tg://user?id={user})"
        body += f'\n{user}: {score}'
    bot.edit_message_text(chat_id=update.message.chat_id,
                      parse_mode='Markdown',
                      message_id=message_id.message_id,
                      text=f"Result: {body}",)


# def echo(update, context):
#     """Echo the user message."""
#     update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    updater = Updater(config['TG_TOKEN'], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", help))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("roll", roll))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
