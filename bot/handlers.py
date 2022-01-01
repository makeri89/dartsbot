from telegram.ext import (
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    Filters
)

import commands
from config import UNAUTHORIZED, NAME, PLAYER, AVERAGE

average_handler = CommandHandler('getaverage', commands.get_average)
average_player_handler = CallbackQueryHandler(commands.average_printer)

start_handler = CommandHandler('start', commands.start)
new_average_handler = CommandHandler('addaverage', commands.users_for_average)

cancel_handler = CommandHandler('cancel', commands.cancel)

conv_handler = ConversationHandler(
    entry_points=[start_handler, new_average_handler],
    states={
        NAME: [
            MessageHandler(Filters.text & ~Filters.command, commands.name)
        ],
        UNAUTHORIZED: [
            MessageHandler(Filters.text & ~Filters.command,
                           commands.unauthorized)
        ],
        PLAYER: [
            CallbackQueryHandler(commands.add_average_choice)
        ],
        AVERAGE: [
            MessageHandler(Filters.text & ~Filters.command, commands.average)
        ]
    },
    fallbacks=[cancel_handler]
)
