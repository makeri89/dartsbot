from telegram.ext import Updater

from util.config import BOT_TOKEN
from bot.handlers import stats_handler, stats_player_handler, \
    conv_handler, help_handler, send_figure_handler

updater = Updater(token=BOT_TOKEN,
                  use_context=True)


def main():
    dispatcher = updater.dispatcher

    dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(stats_player_handler)

    dispatcher.add_handler(help_handler)

    dispatcher.add_handler(send_figure_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
