#!/usr/bin/env python
# pylint: disable=C0116,W0613

import logging
import json
import os
from time import sleep
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# # #   Enable logging   # # #
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
# # #                # # #


# # #   Members   # # #
token = ""
taunt_file_prefix = "Aoe3_taunt_"
taunt_file_postfix = ".ogg"

# # #   Commands   # # #
def help(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Commands:\n/taunt 5 -> Plays taunt number 5 from AoE3')

def send_taunt(update: Update, context: CallbackContext) -> None:
    try:
        taunt = context.args[0]
    except:
        reply_invalid_taunt(update)
        return

    if (not is_taunt_valid(taunt)):
        reply_invalid_taunt(update)
        return
        
    path = os.path.join(os.path.dirname(__file__), "aoe3taunts/" + taunt_file_prefix + taunt + taunt_file_postfix)
    try:
        with open(path, "rb") as f:
            update.message.reply_voice(f)
    except:
        reply_invalid_taunt(update)
# # #                # # #



# # #   Replies   # # #
def reply_invalid_taunt(update: Update):
    update.message.reply_text('Invalid taunt number!')

# # #                # # #


# # #   Validation   # # #
def is_taunt_valid(taunt: str) -> bool:
    try:
        tauntNum = abs(int(taunt))
    except:
        return False
    else:
        return tauntNum >= 1 and tauntNum <= 33
# # #                # # #


# # #   Config   # # #
def load_token_file() -> str:
    with open(os.path.join(os.path.dirname(__file__), "config.json")) as f:
        data = json.load(f)
        return data["token"]
# # #                # # #


# # #   Setup   # # #
def main() -> None:
    """Start the bot."""
    global token
    # Create the Updater and pass it your bot's token.
    token = load_token_file()
    sleep(2)
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("taunt", send_taunt))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
# # #                # # #

if __name__ == '__main__':
    main()