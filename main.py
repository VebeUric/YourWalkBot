from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from Data_Base_Manager import DataBaseManager
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)
from app.OpenSorce import get_interesting_places

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
DELETE_FROM_WISHLIST = chr(19)
SHOW_MY_EVENTS =chr(20)
SCROLL_WISHLIST_BACK, SCROLL_WISHLIST_AHEAD = chr(25), chr(26)
DELETE_FROM_MY_WISHLIST = chr(27)
SHOW_INTERESTING_PLACES = chr(28)
db = DataBaseManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = None
    if update.message:
         username = update.message.from_user.username
    if not db.check_user(username) and update.message:
        db.add_user(username)
    context.user_data["user_id"] = db.get_id_from_username(username)
    text = "Выберите действие"
    buttons = [
        [
            InlineKeyboardButton(
                text="Достопримечательности", callback_data=str(ATTRACTIONS)
            ),
        ],
        [InlineKeyboardButton(text="Мои события", callback_data=str(SHOW_MY_EVENTS))],
        [InlineKeyboardButton(text="Интересные места", callback_data=str(SHOW_INTERESTING_PLACES))],
        [
            InlineKeyboardButton(text="Настройки", callback_data=str(CONFIG)),
        ]

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
    event_id = context.user_data['events'][events[page]]["id"]
    db.add_to_wishlist(event_id, context.user_data["user_id"])
    await update_events(update, context)



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
                  [InlineKeyboardButton(text='Удалить из моих соытий', callback_data=str(DELETE_FROM_WISHLIST))],
                  [InlineKeyboardButton(text="Вернуться в главное меню", callback_data=str(BACK_TO_MENU))]]
    return InlineKeyboardMarkup(markup)

async def update_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    preferences = [tag for tag in context.user_data["pref"].keys() if context.user_data["pref"][tag]]
    events = db.get_events(preferences)
    page = context.user_data["page"]
    print(events)
    print([i.name for i in context.user_data['events'].keys()])
    event_inform = context.user_data['events'].get(events[page])
    text = f"{event_inform['name']} \n" \
           f"{db.get_decription(context.user_data['events'][events[page]]['discription'])}\n" \
           f"{event_inform['adress']}\n{event_inform[events[page]]['phone_number'] if event_inform['phone_number'] else 'Номера телефона нет'}" "\n" \
           f"{event_inform['url'] if event_inform['url'] else 'Ссылки на сайт нет'}"
    print(db.check_in_wishlist(event_inform["id"], context.user_data["user_id"]))
    if db.check_in_wishlist(event_inform["id"], context.user_data["user_id"]):
        markup = get_events_murkup(True)
    else:
        markup = get_events_murkup()
    await update.callback_query.edit_message_text(text=text, reply_markup=markup)
    return SHOW_EVENTS


async def give_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    preferences = [tag for tag in context.user_data["pref"].keys() if context.user_data["pref"][tag]]
    context.user_data['page'] = 0
    events = db.get_events(preferences)
    context.user_data['events'] = {}
    for event in events:
        context.user_data['events'][event] = {}
        context.user_data['events'][event]["id"] = event.id
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

def get_wishlist_murkup():
    markup = [[InlineKeyboardButton("Назад", callback_data=str(SCROLL_WISHLIST_BACK)), InlineKeyboardButton("Вперед", callback_data=str(SCROLL_WISHLIST_AHEAD))],
              [InlineKeyboardButton('Удалить из моих событий', callback_data=str(DELETE_FROM_MY_WISHLIST))],
              [InlineKeyboardButton("Вернуться в главное меню", callback_data=str(BACK_TO_MENU))]
    ]
    return InlineKeyboardMarkup(markup)
async def show_my_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    my_events = db.get_my_events(context.user_data["user_id"])
    if my_events:
        context.user_data['events'] = {}
        context.user_data['page'] = 0
        for event in my_events:
            context.user_data['events'][event] = {}
            context.user_data['events'][event]["id"] = event.id
            context.user_data['events'][event]['name'] = event.name
            context.user_data['events'][event]['discription'] = event.disciption
            context.user_data['events'][event]['adress'] = event.adress
            context.user_data['events'][event]['phone_number'] = event.phone_number
            context.user_data['events'][event]['url'] = event.url
            context.user_data['events'][event]['tag'] = event.tag_id
        text = f"{db.get_decription(context.user_data['events'][my_events[0]]['discription'])}\n" \
               f"{context.user_data['events'][my_events[0]]['adress']}\n{context.user_data['events'][my_events[0]]['phone_number'] if context.user_data['events'][my_events[0]]['phone_number'] else 'Номера телефона нет'}" "\n"\
               f"{context.user_data['events'][my_events[0]]['url'] if context.user_data['events'][my_events[0]]['url'] else 'Ссылки на сайт нет'}"
        await update.callback_query.edit_message_text(text=text, reply_markup=get_wishlist_murkup())
        return SHOW_MY_EVENTS
    else:
        await update.callback_query.edit_message_text(text="Вы не записались ни на одно событие", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Вернуться в главное меню", callback_data=str(BACK_TO_MENU))]]))
        return SHOW_MY_EVENTS


async def update_my_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    page = context.user_data['page']
    my_events = db.get_my_events(context.user_data["user_id"])
    if my_events:
        text = f"{db.get_decription(context.user_data['events'][my_events[0]]['discription'])}\n" \
               f"{context.user_data['events'][my_events[page]]['adress']}\n{context.user_data['events'][my_events[page]]['phone_number'] if context.user_data['events'][my_events[page]]['phone_number'] else 'Номера телефона нет'}" "\n"\
               f"{context.user_data['events'][my_events[page]]['url'] if context.user_data['events'][my_events[page]]['url'] else 'Ссылки на сайт нет'}"
        await update.callback_query.edit_message_text(text=text, reply_markup=get_wishlist_murkup())
        return SHOW_MY_EVENTS
    else:
        await update.callback_query.edit_message_text(text="Вы не записались ни на одно событие", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Вернуться в главное меню", callback_data=str(BACK_TO_MENU))]]))
        return SHOW_MY_EVENTS

async def process_the_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loaction_button = [InlineKeyboardButton('Отправить геопозицию', request_location=True)]
    my_keyboard = InlineKeyboardButton([loaction_button])
    return my_keyboard

def get_places_disc(location):
    text = ""
    places = get_interesting_places(location.split()[0], location.split([1]))
    for place in places:
        pass

async def show_interesting_places(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ll =  44.0448
    lat = 42.8581
    # text = get_places_disc(location)
    # await update.callback_query.edit_message_text(text=text,
    #                                                   reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
    #                                                       "Вернуться в главное меню",
    #                                                       callback_data=str(BACK_TO_MENU))]]))

async def scroll_ahead_wishlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
        number_of_page = context.user_data['page']
        print(number_of_page, context.user_data['events'].keys())
        if number_of_page == len(context.user_data['events'].keys()) - 1:
            context.user_data["page"] = 0
        else:
            context.user_data["page"] += 1
        await update_my_events(update, context)
        return SHOW_MY_EVENTS

async def scroll_back_wishlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
        number_of_page = context.user_data['page']
        if number_of_page - 1 < 0:
            context.user_data["page"] = len(context.user_data['events'].keys() - 1)
        else:
            context.user_data["page"] -= 1
        await update_my_events(update, context)
        return SHOW_MY_EVENTS

async def delete_from_wishlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events = db.get_my_events(context.user_data["user_id"])
    page = context.user_data['page']

    event_id = events[page - 1].id
    db.delete_from_wishlist(context.user_data["user_id"], event_id)
    await update_events(update, context)
    return SHOW_EVENTS
async def delete_from_my_wishlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events = db.get_my_events(context.user_data["user_id"])
    page = context.user_data['page']
    event_id = events[page].id
    print()
    db.delete_from_wishlist(context.user_data["user_id"], event_id)
    await update_my_events(update, context)
    return SHOW_MY_EVENTS

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
        CallbackQueryHandler(show_my_events, pattern="^" + str(SHOW_MY_EVENTS)),
        CallbackQueryHandler(show_interesting_places, pattern="^" + str(SHOW_INTERESTING_PLACES))
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
        CallbackQueryHandler(back_to_choose_tags, pattern="^" + str(BACK_TO_CHOOSE_TAGS)),
        CallbackQueryHandler(delete_from_wishlist, pattern="^" + str(DELETE_FROM_WISHLIST))
    ]
    wishList_scrolling = [
        CallbackQueryHandler(back_to_main_menu, pattern="^" + str(BACK_TO_MENU)),
        CallbackQueryHandler(scroll_ahead_wishlist, pattern="^" + str(SCROLL_WISHLIST_AHEAD)),
        CallbackQueryHandler(scroll_back_wishlist, pattern="^" + str(SCROLL_WISHLIST_BACK)),
        CallbackQueryHandler(delete_from_my_wishlist, pattern="^" + str(DELETE_FROM_MY_WISHLIST))
    ]
    intersting_places = [
        CallbackQueryHandler(back_to_main_menu, pattern="^" + str(BACK_TO_MENU))
    ]
    configs = [
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
            SHOW_MY_EVENTS: wishList_scrolling,
            STOPPING: [CommandHandler("start", start)],
        },
        fallbacks=[CommandHandler("stop", stop)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
