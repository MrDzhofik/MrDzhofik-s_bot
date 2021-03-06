# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import wiki

import random

with open("token.txt", "r") as ftb:
    TOKEN = ftb.readline().strip()


reply_keyboard = [['/address', '/phone'], ['/help', '/close']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def start(update, context):
    update.message.reply_text(
        'Привет! Я подопытный кролик Сириуса!',
        reply_markup=markup
    )


def close_keyboard(update, context):
    update.message.reply_text('ОК', reply_markup=ReplyKeyboardRemove())


def unicode(update, context):
    try:
        number = int(context.args[0])
        if number <= 32:
            update.message.reply_text('Введите число большее, чем 32')
            return 0
        update.message.reply_text(chr(number))
        if number > 65536:
            update.message.reply_text('Введите число меньшее 65536')
    except ValueError:
        update.message.reply_text('Введите число, а не бурку')
    except IndexError:
        update.message.reply_text('Введите после команды число')


def help(update, context):
    update.message.reply_text(
        'Функции: \n/start - информация о боте и запуск кнопочек \n/wiki (слово) - поиск информации в Википедии '
        '\n/address, /phone - тестовые функции, выводят простой текст на экран '
        '\n/unicode (число) - поиск символа UTF-8 по числу \n/set (секунды) - ставим таймер'
        '\n/unset - убираем таймер \n/close - убираем кнопки'
    )


def address(update, context):
    update.message.reply_text('Выдаем на экран какой-то адрес,'
                              ' или ищем его в интернете')


def phone(update, context):
    update.message.reply_text('Идет взлом Пентагона')


def wikipedia(update, context):
    update.message.reply_text("Идет поиск в википедии...")
    print(context.args, " ".join(context.args), "=======")
    context.user_data[str(random.randint(1000000, 9999999))] = (" ".join(context.args))
    result, urlfull = wiki.search_wiki(" ".join(context.args))
    update.message.reply_text(result + urlfull)


def wikipedia_history(update, context):
    update.message.reply_text("История поиска:")
    fstr = ""
    for k in context.user_data:
        fstr += context.user_data[k] + "\n"
    update.message.reply_text(fstr)


def set_timer(update, context):
    chat_id = update.message.chat_id
    try:
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text("Прошлое не вернуть :( !")
            return
        if 'job' in context.chat_data:
            print("найден")
            old_job = context.chat_data['job']
            print(old_job)
            old_job.schedule_removal()
        new_job = context.job_queue.run_repeating(task, due, context=chat_id)
        context.chat_data['job'] = new_job
        update.message.reply_text(f"Повтор каждые {due} секунд")
    except (IndexError, ValueError):
        update.message.reply_text("Использование: /set <секунд>")


def task(context):
    job = context.job
    context.bot.send_message(job.context, text="Я Опять тут!")
    print(context.chat_data)


def unset_timer(update, context):
    if 'job' not in context.chat_data:
        update.message.reply_text("Нет активного таймера")
        return
    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data["job"]
    update.message.reply_text("Работа таймера остановлена!")


def main():
    print('Бот Ванджьашь запущен...')
    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от
    # @BotFather токен
    updater = Updater(TOKEN, use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    # Создаём обработчик сообщений типа Filters.text
    # из описанной выше функции echo()
    # После регистрации обработчика в диспетчере
    # эта функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    help_command = CommandHandler('help', help)
    start_command = CommandHandler('start', start, pass_user_data=True)
    wiki_command = CommandHandler('wiki', wikipedia, pass_user_data=True)
    set_timer_command = CommandHandler('set', set_timer, pass_args=True,
                                       pass_job_queue=True, pass_chat_data=True)
    unset_timer_command = CommandHandler('unset', unset_timer,
                                         pass_chat_data=True)
    unicode_command = CommandHandler('unicode', unicode)
    close_keyboard_command = CommandHandler('close', close_keyboard)
    wiki_history_command = CommandHandler('wikihist', wikipedia_history, pass_user_data=True)

    # Регистрируем обработчик в диспетчере.
    dp.add_handler(start_command)
    dp.add_handler(help_command)
    dp.add_handler(wiki_command)
    dp.add_handler(set_timer_command)
    dp.add_handler(unset_timer_command)
    dp.add_handler(CommandHandler('address', address))
    dp.add_handler(CommandHandler('phone', phone))
    dp.add_handler(close_keyboard_command)
    dp.add_handler(unicode_command)
    dp.add_handler(wiki_history_command)
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
