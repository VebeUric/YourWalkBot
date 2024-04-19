import logging

from flask import Flask

from Data_Base_Manager import DataBaseManager
from typing import Dict
import flask
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data_Base_Models.py/db/DataBase.db'
db = DataBaseManager()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)


logger = logging.getLogger(__name__)

REGISTRATION, START_APP, CHOOSE_PREFRENCE = 1, 2, 3

async def start(update, context):
    print(1111111111111111111111111111111111111)
    if await db.check_user(update.message.from_user.username):
        print(7900000)
        return START_APP
    else:
        print(2222222222222222222222222222222222)
        return REGISTRATION


async def registration(update, context):
    print(3333333333333333333333333333333444444444333333333)
    db.add_user(update.message.from_user.username)
    print(33333333333333333333333333333333333)
    await update.message.reply_text(f"Привет,{update.message.from_user.username}, добро пожаловать в YourWalkBot, я помошник в твоих прогулках ")
    return CHOOSE_PREFRENCE


async def choose_prefernce(update, context):
    prefernces = db.get_all_preferences()



async def close_keyboard(update, context):
    await update.message.reply_text(
        "Хорошо, я запомнил",
        reply_markup=ReplyKeyboardRemove()
    )

async def start_app(update, context):
    pass

async def stop(update, context):
    pass

autification_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            REGISTRATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration)],
            START_APP: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_app)],
            CHOOSE_PREFRENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_prefernce)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )



def main():
    application = Application.builder().token("6509645217:AAEmsdDnEhvRUlDaZwPZlODpGDefPhlzmq8").build()
    application.add_handler(CommandHandler('start_app', start_app))
    application.add_handler(CommandHandler('start', start))

    application.add_handler(autification_conversation_handler)

    application.run_polling()

if __name__ == '__main__':
    if __name__ == '__main__':
        main()
        app.run()