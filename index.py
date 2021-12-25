from telegram.ext import Updater

from config import BOT_TOKEN
from handlers import average_handler, average_player_handler, conv_handler

updater = Updater(token=BOT_TOKEN,
                  use_context=True)

def main():
    dispatcher = updater.dispatcher

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(average_handler)
    dispatcher.add_handler(average_player_handler)

    updater.start_polling()
    
if __name__ == '__main__':
    main()
