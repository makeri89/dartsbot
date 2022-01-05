from telegram.ext import (
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    Filters
)

import bot.commands as commands
import util.config as config

average_handler = CommandHandler('getaverage', commands.get_average)
average_player_handler = CallbackQueryHandler(commands.average_printer)

start_handler = CommandHandler('start', commands.start)
new_average_handler = CommandHandler('addaverage', commands.users_for_average)
new_match_handler = CommandHandler('newmatch', commands.new_match)
new_figure_handler = CommandHandler('figure', commands.figure)

send_figure_handler = CommandHandler('sendfigure', commands.send_figure)

cancel_handler = CommandHandler('cancel', commands.cancel)
help_handler = CommandHandler('help', commands.help_message)

conv_handler = ConversationHandler(
    entry_points=[
        start_handler,
        new_average_handler,
        new_match_handler,
        new_figure_handler
    ],
    states={
        config.NAME: [
            MessageHandler(Filters.text & ~Filters.command, commands.name)
        ],
        config.UNAUTHORIZED: [
            MessageHandler(
                Filters.text & ~Filters.command,
                commands.unauthorized
            )
        ],
        config.PLAYER: [
            CallbackQueryHandler(commands.add_average_choice)
        ],
        config.AVERAGE: [
            MessageHandler(Filters.text & ~Filters.command, commands.average)
        ],
        config.MATCH_AVERAGE: [
            CallbackQueryHandler(commands.match_average)
        ],
        config.DARTS_USED: [
            MessageHandler(Filters.text & ~Filters.command,
                           commands.darts_used)
        ],
        config.HIGHSCORE: [
            MessageHandler(Filters.text & ~Filters.command, commands.highscore)
        ],
        config.SAVE_MATCH: [
            MessageHandler(Filters.text & ~Filters.command,
                           commands.save_score)
        ],
        config.ASK_MORE_PLAYERS: [
            MessageHandler(
                Filters.regex('^(Kyllä|Ei)$'),
                commands.more_players
            )
        ],
        config.FIGURE_PLAYERS: [
            CallbackQueryHandler(commands.player_to_figure)
        ]
    },
    fallbacks=[cancel_handler]
)
