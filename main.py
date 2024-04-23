import logging

from flask import Flask

from Data_Base_Manager import DataBaseManager
from typing import Dict
import flask
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters, CallbackContext,
)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data_Base_Models.py/db/DataBase.db'
db = DataBaseManager()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)




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

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        f"Добрый день, {update.message.from_user.first_name})")
    if db.check_user(update.message.from_user.username):
        return make_location_request(update, context)
    else:
        return await registration(update, context)


async def registration(update, context):
    db.add_user(update.message.from_user.username)
    await update.message.reply_text(f"Добро пожаловать в YourWalkBot, я помошник в твоих прогулках."
                                    f"Я всегда готов помочь, куда бы вы не пошли.")
    return await choose_prefernce(update, context)


def get_keyboard(user_data):
    print(user_data['pref'])
    markup = [[KeyboardButton(f"✅{preference}" if user_data['pref'][preference] else f"❌{preference}")]
                           for preference in user_data.get('pref').keys()]
    markup.append(['Завершить выбор'])
    print(markup)
    return markup
async def choose_prefernce(update, context: CallbackContext):
      prefernces = db.get_all_preferences()
      context.user_data['pref'] = {}
      for i in prefernces:
          context.user_data['pref'][i] = 0
      markup = get_keyboard(context.user_data)
      query = update.callback_query
      print(update.message.text)
      print(query, 11111111111111122222222222222222)
      update.message.reply_text('Чтобы закончить регистрацию, выберте ваши предпочтения', reply_markup=ReplyKeyboardMarkup(markup))
      await btn(update, context)

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

#     context.user_data['prefernces']= {}
#     keyboard = [val for val in prefernces]
#     query = update.callback_query
#     try:
#         await query.answer()
#
#         for i in keyboard:
#             if query.data.preferences.get(i):
#                 context.user_data['preference'][i] = not context.user_data.get("1", False)
#
#         markup = generate_checkboxes(context.user_data)
#         chat_id = update.callback_query.message.chat.id
#         message_id = update.callback_query.message.message_id
#         await context.bot.edit_message_text(
#             "123",
#             chat_id=chat_id,
#             message_id=message_id,
#             reply_markup=ReplyKeyboardMarkup(markup),
#         )
#
#
#
#
#         for prefernce in keyboard:
#             print(prefernce)
#             context.user_data.get('preferences')[prefernce] = 0
#         markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
#         await update.message.reply_text(f"Чтобы завершить регистрацию выбери какие события ты хотел бы получать в своей ленте", reply_markup=markup)
#
#     except:
#          print('hahahha')
#
# def generate_checkboxes(user_data):
#     try:
#         markup = [ReplyKeyboardMarkup(f"✅ {preference}" if user_data['preferences'][preference] else f"❌{preference}")
#                   for preference in user_data.get('preferences').keys()]
#         return markup
#     except:
#         print(5)
#
# async def check_box(update, context):
#     markup = generate_checkboxes(context.user_data)
#     await update.message.reply_text("123", reply_markup=ReplyKeyboardMarkup(markup))


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Хорошо, я запомнил",
        reply_markup=ReplyKeyboardRemove()
    )

async def start_app(update, context):
    pass

async def stop(update, context):
    pass

# async def get_loсaction_message(update, context):
#     location = None
#     await update.message.reply_text(f"Хорошо, чтобы я смог помочь предоставьте ваши геодннаые")
#
#
# async def get_loсaction(update, context):
#     location = update.message.location
#     return f"{location.latitude}{location.longitude}"

def process_the_request():
    loaction_button = [KeyboardButton('Отправить геопозицию', request_location=True)]
    my_keyboard = ReplyKeyboardMarkup([loaction_button])
    return my_keyboard
async def make_location_request(update, context):
    await update.message.reply_text('Отправить геопозицию 🗺️', reply_markup=make_location_request())


main_conv_handler = conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start_app', make_location_request)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )







def main():
    application = Application.builder().token("6509645217:AAEmsdDnEhvRUlDaZwPZlODpGDefPhlzmq8").build()
    application.add_handler(CommandHandler('start_app', start_app))
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('loc', process_the_request))
    application.add_handler(main_conv_handler)
    application.run_polling()

if __name__ == '__main__':
    if __name__ == '__main__':
        main()
        app.run()