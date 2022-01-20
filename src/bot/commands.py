from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup
)
from telegram.ext import (
    CallbackContext,
    ConversationHandler
)

from services.user_service import user_service
from services.average_service import average_service
from services.match_service import match_service
from services.score_service import score_service

from util.plotter import Plotter
from util.logger import logger
import util.config as config


plotter = Plotter()


def player_keyboard(users):
    keyboard = [
        [InlineKeyboardButton(user.name, callback_data=user.id)] for user in users
    ]

    return keyboard


def is_registered(id):
    return user_service.get_user_by_id(id)


def authorize(query):
    return query == config.SECRET


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Kerro nimesi:')
    if context.args and authorize(context.args[0]):
        return config.NAME
    return config.UNAUTHORIZED


def name(update: Update, context: CallbackContext):
    username = update.message.text
    id = update.message.chat.id
    created_user = user_service.create_user(id, username)
    if created_user == 'valid':
        update.message.reply_text('Kiitos, olet nyt rekisteröitynyt.')
    else:
        update.message.reply_text(
            f'Rekisteröityminen epäonnistui, tapahtui seuraava virhe: {created_user}'
        )
        update.message.reply_text('Anna uusi tunnus:')
        return config.NAME

    return ConversationHandler.END


def get_stats(update: Update, context: CallbackContext):
    users = user_service.get_users()
    keyboard = player_keyboard(users)

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Valitse pelaaja:', reply_markup=reply_markup)


def stats_printer(update: Update, context: CallbackContext):
    query = update.callback_query

    average = score_service.get_average(query.data)
    highscore = score_service.get_player_highscore(query.data)

    query.answer()

    if not average['average']:
        query.edit_message_text('Keskiarvoa ei voitu laskea')
    else:
        message = (
            f'Pelaaja: {average["name"]}\n'
            f'Keskiarvo: {average["average"]:.2f}\n'
            f'Highscore: {highscore["highscore"]}'
        )
        query.edit_message_text(message)


def users_for_average(update: Update, context: CallbackContext):
    if is_registered(update.message.chat.id):
        users = user_service.get_users()
        keyboard = player_keyboard(users)

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            'Valitse pelaaja:', reply_markup=reply_markup)

        return config.PLAYER
    return config.UNAUTHORIZED


def add_average_choice(update: Update, context: CallbackContext):
    query = update.callback_query

    global global_user
    global_user = user_service.get_user_by_id(query.data)

    query.answer()
    query.edit_message_text(
        text=f'Valitsit pelaajaksi: {global_user.name}\nSyötä keskiarvo:')

    return config.AVERAGE


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
        return config.MATCH_AVERAGE
    return config.UNAUTHORIZED


def match_average(update: Update, context: CallbackContext):
    query = update.callback_query

    global user_for_match
    user_for_match = query.data

    query.answer()
    query.edit_message_text(text='Syötä keskiarvo:')

    return config.DARTS_USED


def darts_used(update: Update, context: CallbackContext):
    global match_avg
    try:
        match_avg = float(update.message.text)
    except:
        update.message.reply_text('Syötä kelvollinen keskiarvo:')
        return config.DARTS_USED

    update.message.reply_text('Syötä käytettyjen tikkojen määrä:')

    return config.HIGHSCORE


def highscore(update: Update, context: CallbackContext):
    global darts_amount

    try:
        darts_amount = int(update.message.text)
    except:
        darts_amount = 0

    update.message.reply_text('Syötä highscore:')

    return config.SAVE_MATCH


def save_score(update: Update, context: CallbackContext):
    try:
        highscore = int(update.message.text)
    except:
        highscore = 0

    if highscore > 180:
        update.message.reply_text('Syötä kelvollinen highscore')
        return config.SAVE_MATCH

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

    return config.ASK_MORE_PLAYERS


def more_players(update: Update, context: CallbackContext):
    if update.message.text == 'Kyllä':
        logger.info('text was Kyllä')
        users = user_service.get_users()
        keyboard = player_keyboard(users)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            'Lisää pelaaja:', reply_markup=reply_markup)
        return config.MATCH_AVERAGE
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

/getstats \- hae pelaajan tilastot

/figure \- lisää pelaaja kaavioon
• Kaavio kertoo pelaajien keskiarvohistorian

/sendfigure \- lähettää kaavion haluamillasi pelaajilla
• Samalla nollaa kaavioon valitut pelaajat

/cancel \- peru nykyinen toiminto, tyhjennä kaavio
    '''

    update.message.reply_text(message, parse_mode='MarkdownV2')


def figure(update: Update, context: CallbackContext):
    if is_registered(update.message.chat.id):
        users = user_service.get_users()
        keyboard = player_keyboard(users)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            'Lisää pelaaja kaavioon:', reply_markup=reply_markup)
        return config.FIGURE_PLAYERS
    return config.UNAUTHORIZED


def player_to_figure(update: Update, context: CallbackContext):
    query = update.callback_query
    player_id = query.data
    player = user_service.get_user_by_id(player_id)
    averages = score_service.get_all_averages_by_date(player.id)
    start_date = averages[0]['date']
    plotter.plot(averages, start_date, player.name)

    query.answer()
    query.edit_message_text(
        'Pelaaja lisätty!\n\nLisää pelaajia: /figure\n\nHae kaavio: /sendfigure'
    )

    return ConversationHandler.END


def send_figure(update: Update, context: CallbackContext):
    update.message.reply_text('Pieni hetki, kaaviota luodaan...')
    plotter.save()
    with open('./fig.png', 'rb') as image:
        update.message.reply_photo(image)


def highscore_figure(update: Update, context: CallbackContext):
    if is_registered(update.message.chat.id):
        users = user_service.get_users()
        keyboard = player_keyboard(users)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            'Lisää pelaaja kaavioon:', reply_markup=reply_markup)
        return config.HIGHSCORE_FIGURE_PLAYERS
    return config.UNAUTHORIZED


def player_to_highscore_figure(update: Update, context: CallbackContext):
    query = update.callback_query
    player_id = query.data
    player = user_service.get_user_by_id(player_id)
    highscores = score_service.get_all_highscores_by_date(player.id)
    start_date = highscores[0]['date']
    plotter.plot(highscores, start_date, player.name)

    query.answer()
    query.edit_message_text(
        'Pelaaja lisätty!\n\nLisää pelaajia: /highscorefigure\n\nHae kaavio: /sendfigure'
    )

    return ConversationHandler.END
