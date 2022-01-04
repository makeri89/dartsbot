from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    replymarkup
)
from telegram.ext import (
    CallbackContext,
    ConversationHandler
)

from services.user_service import user_service
from services.average_service import average_service
from services.match_service import match_service
from services.score_service import score_service

from plotter import Plotter
from logger import logger

from config import SECRET, UNAUTHORIZED, NAME, PLAYER, \
    AVERAGE, MATCH_AVERAGE, DARTS_USED, HIGHSCORE, SAVE_MATCH, \
    ASK_MORE_PLAYERS, FIGURE_PLAYERS, MORE_PLAYERS_TO_FIGURE


plotter = Plotter()


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
        update.message.reply_text(
            'Valitse pelaaja:', reply_markup=reply_markup)

        return PLAYER
    return UNAUTHORIZED


def get_average(update: Update, context: CallbackContext):
    users = user_service.get_users()
    keyboard = player_keyboard(users)

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Valitse pelaaja:', reply_markup=reply_markup)


def average_printer(update: Update, context: CallbackContext):
    query = update.callback_query

    average = score_service.get_average(query.data)

    query.answer()

    query.edit_message_text(
        text=f'Pelaaja: {average["name"]}, keskiarvo: {average["average"]}')


def add_average_choice(update: Update, context: CallbackContext):
    query = update.callback_query

    global global_user
    global_user = user_service.get_user_by_id(query.data)

    query.answer()
    query.edit_message_text(
        text=f'Valitsit pelaajaksi: {global_user.name}\nSyötä keskiarvo:')

    return AVERAGE


def average(update: Update, context: CallbackContext):
    average = float(update.message.text)
    average_service.add_average(global_user, average)

    update.message.reply_text('Keskiarvo tallennettu!')

    return ConversationHandler.END


def new_match(update: Update, context: CallbackContext):
    if is_registered(update.message.chat.id):
        global current_match_id
        current_match_id = match_service.add_match()
        update.message.reply_text('Uusi peli luotu!')
        users = user_service.get_users()
        keyboard = player_keyboard(users)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            'Lisää pelaaja:', reply_markup=reply_markup)
        return MATCH_AVERAGE
    return UNAUTHORIZED


def match_average(update: Update, context: CallbackContext):
    query = update.callback_query

    global user_for_match
    user_for_match = query.data

    query.answer()
    query.edit_message_text(text='Syötä keskiarvo:')

    return DARTS_USED


def darts_used(update: Update, context: CallbackContext):
    global match_avg
    try:
        match_avg = float(update.message.text)
    except:
        update.message.reply_text('Syötä kelvollinen keskiarvo:')
        return DARTS_USED

    update.message.reply_text('Syötä käytettyjen tikkojen määrä:')

    return HIGHSCORE


def highscore(update: Update, context: CallbackContext):
    global darts_amount

    try:
        darts_amount = int(update.message.text)
    except:
        darts_amount = 0

    update.message.reply_text('Syötä highscore:')

    return SAVE_MATCH


def save_score(update: Update, context: CallbackContext):
    try:
        highscore = int(update.message.text)
    except:
        highscore = 0

    score_service.add_score(
        current_match_id,
        user_for_match,
        match_avg,
        darts_amount,
        highscore
    )

    update.message.reply_text('Pelaajan tulos lisätty!')

    keyboard = [
        ['Kyllä'],
        ['Ei']
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text(
        'Lisää pelaaja:', reply_markup=reply_markup)

    return ASK_MORE_PLAYERS


def more_players(update: Update, context: CallbackContext):
    if update.message.text == 'Kyllä':
        logger.info('text was Kyllä')
        users = user_service.get_users()
        keyboard = player_keyboard(users)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            'Lisää pelaaja:', reply_markup=reply_markup)
        return MATCH_AVERAGE
    else:
        update.message.reply_text('Peli tallennettu!')
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    logger.info('Cancelled')
    update.message.reply_text('Peruit toiminnon')

    plotter.clear()

    return ConversationHandler.END


def unauthorized(update: Update, context: CallbackContext):
    logger.info('Unauthorized access tried')
    update.message.reply_text(
        'Unauthorized access, please ask admin for a joining link')

    return ConversationHandler.END


def help_message(update: Update, context: CallbackContext):
    message = '''
*Botti dartspelien tallentamiseen*

Komennot:

/start \- luo uusi käyttäjä
\(toimii vain rekisteröitymislinkin kautta\)

/newmatch \- lisää uusi peli
• Voit lisätä useamman pelaajan kerralla
• Keskiarvo on ainoa pakollinen tieto
• Voit ohittaa muut tiedot lähettämällä jotain muuta kuin numeron

/getaverage \- hae pelaajan keskiarvo

/figure \- lisää pelaaja kaavioon
• Kaavio kertoo pelaajien keskiarvohistorian

/sendfigure \- lähettää kaavion haluamillasi pelaajilla

/cancel \- peru nykyinen toiminto, tyhjennä kuvaaja
    '''

    update.message.reply_text(message, parse_mode='MarkdownV2')


def figure(update: Update, context: CallbackContext):
    if is_registered(update.message.chat.id):
        users = user_service.get_users()
        keyboard = player_keyboard(users)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            'Lisää pelaaja kaavioon:', reply_markup=reply_markup)
        return FIGURE_PLAYERS
    return UNAUTHORIZED


def player_to_figure(update: Update, context: CallbackContext):
    query = update.callback_query
    player_id = query.data
    player = user_service.get_user_by_id(player_id)
    averages = score_service.get_all_averages_by_date(player.id)
    start_date = averages[0]['date']
    plotter.plot(averages, start_date, player.name)

    query.answer()
    query.edit_message_text('Pelaaja lisätty!')

    return ConversationHandler.END


def send_figure(update: Update, context: CallbackContext):
    # if update.message.text == 'Haluan kaavioni':
    plotter.save()
    with open('./fig.png', 'rb') as image:
        update.message.reply_photo(image)
    return ConversationHandler.END

    # if update.message.text == 'Lisää pelaajia':
    #     users = user_service.get_users()
    #     keyboard = player_keyboard(users)
    #     reply_markup = InlineKeyboardMarkup(keyboard)
    #     update.message.reply_text(
    #         'Lisää pelaaja kaavioon:', reply_markup=reply_markup)
    #     return FIGURE_PLAYERS
