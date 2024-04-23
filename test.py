from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Application


# Функция для создания клавиатуры
def create_keyboard(preferences):
    button_values = ["Значение 1", "Значение 2", "Значение 3"]
    keyboard = [[f"{int(preferences.get(value, 0))} {value}"] for value in button_values]
    return ReplyKeyboardMarkup(keyboard)


# Команда для отображения клавиатуры
def start(update, context):
    # Если в контексте нет данных о предпочтениях, установите их в пустой словарь
    if 'preferences' not in context.user_data:
        context.user_data['preferences'] = {}

    # Создание клавиатуры с учетом текущих предпочтений
    keyboard = create_keyboard(context.user_data['preferences'])

    update.message.reply_text('Выберите предпочтение:', reply_markup=keyboard)


# Обработчик для обновления предпочтений
def update_preference(update, context):
    # Извлекаем текст кнопки
    preference = update.message.text

    # Извлекаем значение предпочтения (нуль или единица) из начала названия кнопки
    value = int(preference.split()[0])

    # Извлекаем само предпочтение (без начального значения)
    preference_name = ' '.join(preference.split()[1:])

    # Обновляем предпочтение в контексте
    context.user_data['preferences'][preference_name] = 1 - value

    # Обновляем клавиатуру с учетом новых предпочтений
    keyboard = create_keyboard(context.user_data['preferences'])

    update.message.reply_text('Предпочтение обновлено. Выберите новое предпочтение:', reply_markup=keyboard)


# Создание и запуск бота
def main():
    application = Application.builder().token("6509645217:AAEmsdDnEhvRUlDaZwPZlODpGDefPhlzmq8").build()
    application.add_handler(CommandHandler('start', update_preference))
    application.add_handler(MessageHandler(Fil))
    application.run_polling()
    application.idle()


if __name__ == '__main__':
    main()