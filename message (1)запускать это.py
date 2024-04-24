import logging

# from flask import Flask
from app.geocder import Geocodere
from Data_Base_Manager import DataBaseManager
from typing import Dict
# import flask
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import (CallbackQueryHandler,
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters, CallbackContext,
)
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data_Base_Models.py/db/DataBase.db'
db = DataBaseManager()
gd = Geocodere()
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
#
# logger = logging.getLogger(__name__)




async def do_request_for_nearest(args):
    pass

async def get_interesting_places(args):
    pass

actions = {
'Найди ближай': do_request_for_nearest,
'Где можно': do_request_for_nearest,

'Что можно посмотреть': get_interesting_places,
'Куда бы сходить': get_interesting_places
}




REGISTRATION, START_APP, CHOOSE_PREFRENCE = 1, 2, 3
FIND_PLACE_NEAREST = 4
ABOUT = 5


async def start(update: Update, context: CallbackContext) -> None:
    context.user_data['chat_id'] = update.message.chat_id
    await update.message.reply_text(
        f"Добрый день, {update.message.from_user.first_name})")
    # if db.check_user(update.message.from_user.username):
    #     return await make_location_request(update, context)
    # else:
    return await registration(update, context)


async def registration(update, context):
    await update.message.reply_text(f"Добро пожаловать в YourWalkBot, я помошник в твоих прогулках."
                                    f"Я всегда готов помочь, куда бы вы не пошли.")
    return await choose_prefernce(update, context)


def get_keyboard(user_data):
    print(user_data['pref'])
    markup = [[KeyboardButton(f"✅{preference}" if user_data['pref'][preference] else f"❌{preference}")]
                           for preference in user_data.get('pref').keys()]
    markup.append(['Завершить выбор'])
    return markup

async def choose_prefernce(update, context: CallbackContext):
      prefernces = db.get_all_preferences()
      context.user_data['pref'] = {}
      for i in prefernces:
          context.user_data['pref'][i] = 0
      markup = get_keyboard(context.user_data)
      await update.message.reply_text('Чтобы закончить регистрацию, выберте ваши предпочтения', reply_markup=ReplyKeyboardMarkup(markup))

async def btn(update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if update.message.text == "❌Велопоездки":
        context.user_data["pref"]['❌Велопоездки'] = not context.user_data['pref'].get("❌Велопоездки", False)

    markup = get_keyboard(context.user_data)
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    await context.bot.edit_message_text(
        "Чтобы закончить регистрацию, выберте ваши предпочтения",
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=ReplyKeyboardMarkup(markup),
    )

async def close_keyboard(update, context):
    for val in context.user_data['pref'].keys():
        if context.user_data['pref'][val]:
            db.pass_preference(update.message.from_user.username, db.get_tag_id_from_name(val))
    await update.message.reply_text(
        "Хорошо, я запомнил",
        reply_markup=ReplyKeyboardRemove()
    )
    await make_location_request(update, context)
    await main_menu(update, context)

async def start_app(update, context):
    pass

async def stop(update, context):
    pass



def process_the_request():
    loaction_button = [KeyboardButton('Отправить геопозицию 🗺️', request_location=True)]
    my_keyboard = ReplyKeyboardMarkup([loaction_button])
    return my_keyboard

async def make_location_request(update, context):
    await update.message.reply_text('Отправьте свою геопозицию чтобы я мог вам помочь', reply_markup=process_the_request())
    


async def change_keyboard(update, context):
        if not update.message.text == 'Завершить выбор':
            for tag in context.user_data['pref'].keys():
                if tag in update.message.text:
                    context.user_data['pref'][tag] = int(not context.user_data['pref'][tag])
            markup = get_keyboard(context.user_data)

            message = (await update.message.reply_text('Выбрано: ', reply_markup = ReplyKeyboardMarkup(markup)))
        else:
            await close_keyboard(update, context)



async def find_place(update, context):
    await update._bot.send_message(text='Хорошо', chat_id=context.user_data['chat_id'])
    gd.set_place(update.message.text)
    ll = update.message.from_user.location
    print(ll)

async def find_place_nearest(update, context):
    await update._bot.send_message(text='Какое место вы ищите?', chat_id=context.user_data['chat_id'])
    return find_place(update, context)


async def about(update: Update, context):
    await update._bot.send_message(text='Сейчас найду', chat_id=context.user_data['chat_id'])


async def foo_call_back_processing(update: Update, context: CallbackContext):
    query = update.callback_query.data
    print(query)
    if query == 'mnfind_place_nearest':
        return await  find_place_nearest(update, context)
    if query == "mnfind_about":
        return await about(update, context)

async def main_menu(update, context):
    murkup = [
        [InlineKeyboardButton('Найти место поблизости', callback_data='mnfind_place_nearest')],
        [InlineKeyboardButton(text='Узнать об достопримечательности', callback_data='mnfind_about')],
        [InlineKeyboardButton(text='Порекомендовать место', callback_data='mnrecomend_place')],
        [InlineKeyboardButton(text='Посмотерть ленту', callback_data='mnsee_lent')],
        [InlineKeyboardButton(text='Посмотерть свои события', callback_data='mnlook_my_events')],
        [InlineKeyboardButton(text='Изменить предпочтения', callback_data='mnchanges_prefers')]
    ]
    await update.message.reply_text('Главное меню', reply_markup=InlineKeyboardMarkup(murkup))



def main():
    application = Application.builder().token("6509645217:AAEmsdDnEhvRUlDaZwPZlODpGDefPhlzmq8").build()
    application.add_handler(CommandHandler('start_app', start_app))
    application.add_handler(CommandHandler('start', start))

    change_tags = MessageHandler(filters.TEXT, change_keyboard)
    application.add_handler(change_tags)
    application.add_handler(CallbackQueryHandler(foo_call_back_processing))
    application.run_polling()

if __name__ == '__main__':
    if __name__ == '__main__':
        main()
