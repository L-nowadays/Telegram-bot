from telegram.ext import Updater, CommandHandler, RegexHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from random import shuffle, choice

right_phrases = ['Как не странно, но вы правы!', 'Верный ответ!', 'Вам повезло, это верный ответ!']
win_money_sizes = [500, 1000,
                   2000, 3000,
                   5000, 10000,
                   15000, 25000,
                   50000, 100000,
                   200000, 400000,
                   800000, 1500000,
                   300000]

# Keyboards
main_menu = ReplyKeyboardMarkup([['Правила'], ['Начать игру']])

# Prepare questions
with open('questions.txt', encoding='utf-8') as file:
    data = file.read().split('\n')
    questions = []
    for i in data:
        parts = i.split('|')
        question, answers = parts[0], parts[1:]
        questions.append([question, answers])
# shuffle questions and take first 15 for game
shuffle(questions)
questions = questions[:15]
# Current question
curr_question = -1


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


# Functions for game states
def next_question(bot, update):
    global curr_question
    if curr_question != -1:
        update.message.reply_text('{} Следующий вопрос...'.format(choice(right_phrases)))
    curr_question += 1
    if curr_question == 15:
        update.message.reply_text('Поздравляю, вы только что выйграли 3 000 000 рублей!!!!!!')
        return ConversationHandler.END
    else:
        update.message.reply_text('Цена вопроса: {} рублей.'.format(win_money_sizes[curr_question]))
        question_answers = questions[curr_question]
        # Answers for  question
        answers = question_answers[1]
        keyboard = ReplyKeyboardMarkup([*map(lambda x: [x.rstrip('/r')], answers)])
        # Ask question
        question = question_answers[0]
        update.message.reply_text(question, reply_markup=keyboard)
        return curr_question


# Unplanned exit
def end_game(bot, update):
    update.message.reply_text('Игра окончена.', reply_markup=main_menu)


# Wrong answer exit
def lose(bot, update):
    global curr_question
    answers = questions[curr_question][1]
    right_answer = [i.rstrip('/r') for i in answers if i.endswith('/r')][0]
    update.message.reply_text('К сожалению, правильный ответ "{}", это проигрыш.'.format(right_answer),
                              reply_markup=main_menu)
    curr_question = -1

    return ConversationHandler.END


# Main
def main():
    updater = Updater("586280341:AAGYI6FGnyCBHvtBxA3YIe62ZcYCsxjz4JQ")

    # Dispatcher
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(RegexHandler('Правила', rules))

    # Conversation handler
    conv_states = {}
    for i in range(15):
        question, answers = questions[i]
        right_answer = [i.rstrip('/r') for i in answers if i.endswith('/r')][0]
        answers = list(map(lambda x: x.rstrip('/r'), answers))
        answers.remove(right_answer)
        shuffle(answers)
        handlers = [RegexHandler(right_answer, next_question), *[RegexHandler(i, lose) for i in answers]]
        conv_states[i] = handlers
    dp.add_handler(ConversationHandler(
        entry_points=[RegexHandler('Начать игру', next_question)],
        states=conv_states,
        fallbacks=[CommandHandler('end_game', end_game)]
    ))
    # Main loop
    updater.start_polling()

    # Exit case
    updater.idle()


if __name__ == '__main__':
    main()
