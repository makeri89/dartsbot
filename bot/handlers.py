from telegram.ext import (
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    Filters
)

import commands
from config import UNAUTHORIZED, NAME, PLAYER, \
    AVERAGE, MATCH_AVERAGE, DARTS_USED, HIGHSCORE, \
    SAVE_MATCH, ASK_MORE_PLAYERS

average_handler = CommandHandler('getaverage', commands.get_average)
average_player_handler = CallbackQueryHandler(commands.average_printer)

start_handler = CommandHandler('start', commands.start)
new_average_handler = CommandHandler('addaverage', commands.users_for_average)
new_match_handler = CommandHandler('newmatch', commands.new_match)

cancel_handler = CommandHandler('cancel', commands.cancel)
help_handler = CommandHandler('help', commands.help_message)

conv_handler = ConversationHandler(
    entry_points=[start_handler, new_average_handler, new_match_handler],
    states={
        NAME: [
            MessageHandler(Filters.text & ~Filters.command, commands.name)
        ],
        UNAUTHORIZED: [
            MessageHandler(
                Filters.text & ~Filters.command,
                commands.unauthorized
            )
        ],
        PLAYER: [
            CallbackQueryHandler(commands.add_average_choice)
        ],
        AVERAGE: [
            MessageHandler(Filters.text & ~Filters.command, commands.average)
        ],
        MATCH_AVERAGE: [
            CallbackQueryHandler(commands.match_average)
        ],
        DARTS_USED: [
            MessageHandler(Filters.text & ~Filters.command,
                           commands.darts_used)
        ],
        HIGHSCORE: [
            MessageHandler(Filters.text & ~Filters.command, commands.highscore)
        ],
        SAVE_MATCH: [
            MessageHandler(Filters.text & ~Filters.command,
                           commands.save_score)
        ],
        ASK_MORE_PLAYERS: [
            MessageHandler(
                Filters.regex('^(Kyllä|Ei)$'),
                commands.more_players
            )
        ]
    },
    fallbacks=[cancel_handler]
)
