from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    CallbackContext,
    ConversationHandler
)

from services.user_service import user_service
from services.average_service import average_service

from logger import logger

from config import SECRET, UNAUTHORIZED, NAME, PLAYER, AVERAGE

def player_keyboard(users):
    keyboard = [
        [InlineKeyboardButton(user.name, callback_data=user.id)] for user in users
    ]
    
    return keyboard

def is_registered(id):
    return user_service.get_user_by_id(id)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Kerro nimesi:')
    if context.args and context.args[0] == SECRET:
        return NAME
    return UNAUTHORIZED

def name(update: Update, context: CallbackContext):
    username = update.message.text
    id = update.message.chat.id
    user_service.create_user(id, username)
    update.message.reply_text('Kiitos, olet nyt rekisteröitynyt.')
    
    return ConversationHandler.END

def users_for_average(update: Update, context: CallbackContext):
    if is_registered(update.message.chat.id):
        users = user_service.get_users()
        keyboard = player_keyboard(users)

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Valitse pelaaja:', reply_markup=reply_markup)

        return PLAYER
    return UNAUTHORIZED

def get_average(update: Update, context: CallbackContext):
    users = user_service.get_users()
    keyboard = player_keyboard(users)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Valitse pelaaja:', reply_markup=reply_markup)

def average_printer(update: Update, context: CallbackContext):
    query = update.callback_query
    
    user = user_service.get_user_by_id(query.data)
    
    average = average_service.get_user_average(user)
    
    query.answer()
    
    query.edit_message_text(text=f'Pelaaja: {average[0]}, keskiarvo: {average[1]}')

def add_average_choice(update: Update, context: CallbackContext):
    query = update.callback_query
        
    global global_user
    global_user = user_service.get_user_by_id(query.data)
    
    query.answer()
    query.edit_message_text(text=f'Valitsit pelaajaksi: {global_user.name}\nSyötä keskiarvo:')
    
    return AVERAGE

def average(update: Update, context: CallbackContext):
    average = float(update.message.text)
    average_service.add_average(global_user, average)
    
    update.message.reply_text('Keskiarvo tallennettu!')
    
    return ConversationHandler.END
    
def cancel(update: Update, context: CallbackContext):
    logger.info('Cancelled')
    update.message.reply_text('Peruit rekisteröitymisen')
    
    return ConversationHandler.END
    
def unauthorized(update: Update, context: CallbackContext):
    logger.info('Unauthorized access tried')
    update.message.reply_text('Unauthorized access, please ask admin for a joining link')
    
    return ConversationHandler.END
