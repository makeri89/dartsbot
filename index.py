import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    Filters
)

from services.user_service import user_service
from services.average_service import average_service

from config import BOT_TOKEN

updater = Updater(token=BOT_TOKEN,
                  use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

UNAUTHORIZED, NAME, PLAYER, AVERAGE = 0, 1, 2, 3

global_user = None

def player_keyboard():
    users = user_service.get_users()
    keyboard = [
        [InlineKeyboardButton(user.name, callback_data=user.id)] for user in users
    ]
    
    return keyboard

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Kerro nimesi:')
    if context.args and context.args[0] == 'testi':
        return NAME
    return UNAUTHORIZED

def name(update: Update, context: CallbackContext):
    username = update.message.text
    id = update.message.chat.id
    user_service.create_user(id, username)
    update.message.reply_text('Kiitos, olet nyt rekisteröitynyt.')
    
    return ConversationHandler.END

def add_average(update: Update, context: CallbackContext):
    keyboard = player_keyboard()
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Valitse pelaaja:', reply_markup=reply_markup)
    
    return PLAYER

def get_average(update: Update, context: CallbackContext):
    keyboard = player_keyboard()
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Valitse pelaaja:', reply_markup=reply_markup)

def average_printer(update: Update, context: CallbackContext):
    query = update.callback_query
    
    user = user_service.get_user_by_id(query.data)
    
    average = average_service.get_user_average(user)
    
    query.answer()
    
    query.edit_message_text(text=f'Pelaaja: {average[0]}, keskiarvo: {average[1]}')

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    
    query.answer()
    
    global global_user
    global_user = user_service.get_user_by_id(query.data)
    
    logger.info(global_user)
    
    query.edit_message_text(text=f'Valitsit pelaajaksi: {global_user.name}\nSyötä keskiarvo:')
    
    logger.info(AVERAGE)
    
    return AVERAGE

def average(update: Update, context: CallbackContext):
    average = float(update.message.text)
    average_service.add_average(global_user, average)
    
    return ConversationHandler.END
    
def cancel(update: Update, context: CallbackContext):
    logger.info('Cancelled')
    update.message.reply_text('Peruit rekisteröitymisen')
    
    return ConversationHandler.END
    
def unauthorized(update: Update, context: CallbackContext):
    logger.info('Unauthorized access tried')
    update.message.reply_text('Unauthorized access, please ask admin for a joining link')
    
    return ConversationHandler.END

start_handler = CommandHandler('start', start)
new_average_handler = CommandHandler('addaverage', add_average)

cancel_handler = CommandHandler('cancel', cancel)

conv_handler = ConversationHandler(
    entry_points=[start_handler, new_average_handler],
    states={
        NAME: [
            MessageHandler(Filters.text & ~Filters.command, name)
        ],
        UNAUTHORIZED: [
            MessageHandler(Filters.text & ~Filters.command, unauthorized)
        ],
        PLAYER: [
            CallbackQueryHandler(button)
        ],
        AVERAGE: [
            MessageHandler(Filters.text & ~Filters.command, average)
        ]
    },
    fallbacks=[cancel_handler]
)

def main():
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler('getaverage', get_average))
    dispatcher.add_handler(CallbackQueryHandler(average_printer))

    updater.start_polling()
    
if __name__ == '__main__':
    main()
