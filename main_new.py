from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from Data_Base_Manager import DataBaseManager
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

# main menu
SELECTING_ACTION, ATTRACTIONS, CONFIG = map(chr, range(3))

(START_OVER,) = map(chr, range(3, 4))

CHOICE = chr(6)
CHOISE_TYPES = chr(7)
BACK_TO_MENU = chr(9)
STOPPING = chr(8)
CHOOSE_ALL = chr(11)
SHOW_EVENTS_BUTTON = chr(12)
SCROLL_AHEAD = chr(13)
SCROLL_BACK = chr(14)
ADD_TO_WISHLIST = chr(15)
SHOW_EVENTS = chr(16)
BACK_TO_CHOOSE_TAGS = chr(17)

db = DataBaseManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    if db.check_user(username):

    text = "Выберите действие"
    buttons = [
        [
            InlineKeyboardButton(
                text="Достопримечательности", callback_data=str(ATTRACTIONS)
            ),
        ],
        [
            InlineKeyboardButton(text="Настройки", callback_data=str(CONFIG)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        await update.message.reply_text(text=text, reply_markup=keyboard)

    return SELECTING_ACTION


def get_keyboard(user_data):
    markup = [
        [
            InlineKeyboardButton(
                (
                    f"✅{preference}"
                    if user_data["pref"][preference]
                    else f"❌{preference}"
                ),
                callback_data=f"{CHOICE}:{preference}",
            )
        ]
        for choice_id, preference in enumerate(user_data.get("pref").keys())
    ]
    markup.append([InlineKeyboardButton(text="Показать", callback_data=str(SHOW_EVENTS_BUTTON)), InlineKeyboardButton(text="Выбрать всё", callback_data=str(CHOOSE_ALL))])
    markup.append([InlineKeyboardButton(text="Вернуться в главное меню", callback_data=str(BACK_TO_MENU))])
    return markup


def get_from_db(user_data):
    if not user_data.get("pref"):
        user_data["pref"] = {}
        for item in db.get_all_preferences():
            user_data["pref"][item] = False


async def show_attractions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Выбирайте категории"
    get_from_db(context.user_data)
    buttons = get_keyboard(context.user_data)
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return CHOISE_TYPES


def edint_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def update_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice_type = update.callback_query.data.split(":")[-1]
    context.user_data["pref"][choice_type] = not context.user_data["pref"][choice_type]
    return await show_attractions(update, context)
    # return CHOISE_TYPES

async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[START_OVER] = True
    await start(update, context)
    return SELECTING_ACTION


async def choose_all_tags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for tag in context.user_data["pref"].keys():
        context.user_data["pref"][tag] = True
    await show_attractions(update, context)


async def show_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def scroll_ahead(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number_of_page = context.user_data['page']
    print(number_of_page, context.user_data['events'].keys())
    if number_of_page == len(context.user_data['events'].keys()) - 1:
        context.user_data["page"] = 0
    else:
        context.user_data["page"] += 1
    await update_events(update, context)
    return SHOW_EVENTS


async def scroll_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number_of_page = context.user_data['page']
    if number_of_page - 1 < 0:
        context.user_data["page"] = len(context.user_data['events'].keys() - 1)
    else:
        context.user_data["page"] -= 1
    await update_events(update, context)
    return SHOW_EVENTS

async def add_to_wishlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    page = context.user_data["page"]
    preferences = [tag for tag in context.user_data["pref"].keys() if context.user_data["pref"][tag]]
    events = db.get_events(preferences)
    event_id = context.user_data['events'][events[page]]
    db.add_to_wishlist()


async def back_to_choose_tags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update_choice(update, context)
    return CHOISE_TYPES


def get_events_murkup(is_added=False):
    if not is_added:
        markup = [[InlineKeyboardButton(text='Назад', callback_data=str(SCROLL_BACK)), InlineKeyboardButton(text="Вперед", callback_data=str(SCROLL_AHEAD))],
                  [InlineKeyboardButton(text='Добавить в мои события', callback_data=str(ADD_TO_WISHLIST))],
                  [InlineKeyboardButton(text="Вернуться в главное меню", callback_data=str(BACK_TO_MENU))]]
    else:
        markup = markup = [[InlineKeyboardButton(text='Назад', callback_data=str(SCROLL_BACK)), InlineKeyboardButton(text="Вперед", callback_data=str(SCROLL_AHEAD))],
                  [InlineKeyboardButton(text='Удалить из моих соытий', callback_data=str(ADD_TO_WISHLIST))],
                  [InlineKeyboardButton(text="Вернуться в главное меню", callback_data=str(BACK_TO_MENU))]]
    return InlineKeyboardMarkup(markup)

async def update_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    preferences = [tag for tag in context.user_data["pref"].keys() if context.user_data["pref"][tag]]
    events = db.get_events(preferences)
    page = context.user_data["page"]
    print(page, events)
    print(context.user_data['events'])
    text = f"{db.get_decription(context.user_data['events'][events[page]]['discription'])}\n" \
           f"{context.user_data['events'][events[page]]['adress']}\n{context.user_data['events'][events[page]]['phone_number'] if context.user_data['events'][events[0]]['phone_number'] else 'Номера телефона нет'}" "\n"\
           f"{context.user_data['events'][events[page]]['url'] if context.user_data['events'][events[page]]['url'] else 'Ссылки на сайт нет'}"
    print('zdssssssssssssssssssssssssssssssssssssssss')
    await update.callback_query.edit_message_text(text=text, reply_markup=get_events_murkup())
    print(page)
    return SHOW_EVENTS


async def give_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    preferences = [tag for tag in context.user_data["pref"].keys() if context.user_data["pref"][tag]]
    context.user_data['page'] = 0
    events = db.get_events(preferences)
    context.user_data['events'] = {}
    for event in events:
        context.user_data['events'][event] = {}
        context.user_data['events'][event]['name'] = event.name
        context.user_data['events'][event]['discription'] = event.disciption
        context.user_data['events'][event]['adress'] = event.adress
        context.user_data['events'][event]['phone_number'] = event.phone_number
        context.user_data['events'][event]['url'] = event.url
        context.user_data['events'][event]['tag'] = event.tag_id
    print(context.user_data['events'], 45454545)
    print(context.user_data['events'][events[1]], 45454545)
    text = f"{db.get_decription(context.user_data['events'][events[0]]['discription'])}\n" \
           f"{context.user_data['events'][events[0]]['adress']}\n{context.user_data['events'][events[0]]['phone_number'] if context.user_data['events'][events[0]]['phone_number'] else 'Номера телефона нет'}" "\n"\
           f"{context.user_data['events'][events[0]]['url'] if context.user_data['events'][events[0]]['url'] else 'Ссылки на сайт нет'}"
    await update.callback_query.edit_message_text(text=text, reply_markup=get_events_murkup())
    return SHOW_EVENTS


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token("6509645217:AAEmsdDnEhvRUlDaZwPZlODpGDefPhlzmq8")
        .build()
    )

    main_menu_handlers = [
        CallbackQueryHandler(show_attractions, pattern="^" + str(ATTRACTIONS) + "$"),
        CallbackQueryHandler(edint_config, pattern="^" + str(CONFIG) + "$"),
    ]

    choice_menu_attractions = [
        CallbackQueryHandler(update_choice, pattern="^" + str(CHOICE) + ":"),
        CallbackQueryHandler(back_to_main_menu, pattern="^" + str(BACK_TO_MENU)),
        CallbackQueryHandler(choose_all_tags, pattern="^" + str(CHOOSE_ALL)),
        CallbackQueryHandler(give_events, pattern="^" + str(SHOW_EVENTS_BUTTON))
    ]
    events_scrollings_handler = [
        CallbackQueryHandler(scroll_ahead, pattern="^"+ str(SCROLL_AHEAD)),
        CallbackQueryHandler(scroll_back, pattern="^" + str(SCROLL_BACK)),
        CallbackQueryHandler(add_to_wishlist, pattern="^" + str(ADD_TO_WISHLIST)),
        CallbackQueryHandler(back_to_main_menu, pattern="^" + str(BACK_TO_MENU)),
        CallbackQueryHandler(back_to_choose_tags, pattern="^" + str(BACK_TO_CHOOSE_TAGS))
    ]
    WishList_scrolling = [
        CallbackQueryHandler(back_to_main_menu, pattern="^" + str(BACK_TO_MENU))
    ]
    # Set up top level ConversationHandler (selecting action)
    # Because the states of the third level conversation map to the ones of the second level
    # conversation, we need to make sure the top level conversation can also handle them

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECTING_ACTION: main_menu_handlers,
            CHOISE_TYPES: choice_menu_attractions,
            SHOW_EVENTS: events_scrollings_handler,
            STOPPING: [CommandHandler("start", start)],
        },
        fallbacks=[CommandHandler("stop", stop)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
