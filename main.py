from telegram.ext import Updater, CommandHandler, RegexHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup

# Keyboards
main_menu = ReplyKeyboardMarkup([['Правила'], ['Начать игру']])


# Functions for commands
def start(bot, update):
    update.message.reply_text('Привет, я бот - игра\n"Кто хочет стать миллионером?"*' + ' Хочешь получить 3 миллиона?' +
                              ' Тогда ответь на 15 вопросов разного уровня сложности! ' + 'Будет весело :)' +
                              '\n*Этот бот - шутка, и, разумеется, никакой выйгрыш забрать не получится.',
                              reply_markup=main_menu)


def rules(bot, update):
    update.message.reply_text('Правила игры:' +
                              '\n1. У каждого вопроса есть 4 варианта ответа, причем только 1 из них верный.' +
                              '\n2. Если в при ответе возникают затруднения, то можно воспользоваться одним' +
                              ' из 3 одноразовых бонусов:' +
                              '\na) 50:50 - компьютер убирает 2 неверный варианта ответа.' +
                              '\nб) Звонок другу - нет, не настоящий звонок другу, я буду в роле друга и предложу' +
                              ' вариант ответа. Cкорее всего, он будет верным, но кто знает...я тоже могу ошибаться.' +
                              '\nв) Помощь зала - великие и не очень знатоки из зала поделятся своим мнением.*' +
                              '\n*Рядом с каждым вариантом будет подписан процент людей, считающих его верным.')


def start_game(bot, update):
    pass


# Main
def main():
    updater = Updater("586280341:AAGYI6FGnyCBHvtBxA3YIe62ZcYCsxjz4JQ")

    # Dispatcher
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(RegexHandler('Правила', rules))

    # Conversation handler
    dp.add_handler(ConversationHandler(
        entry_points=[RegexHandler('Начать игру', start_game)],
        states={},
        fallbacks=[]
    ))
    # Main loop
    updater.start_polling()

    # Exit case
    updater.idle()


if __name__ == '__main__':
    main()
