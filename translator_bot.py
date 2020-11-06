import telebot
from translator import translator
import shelve
import os

TRANCLATOR = os.getenv("TRANSLATOR")
bot = telebot.TeleBot(TRANCLATOR)
lang = [b'\xF0\x9F\x87\xB7\xF0\x9F\x87\xBA'.decode() + ' Russian',
        'Arabic',
        b'\xF0\x9F\x87\xA9\xF0\x9F\x87\xAA	'.decode() + ' German',
        b'\xF0\x9F\x87\xBA\xF0\x9F\x87\xB8'.decode() + '  English',
        b'\xF0\x9F\x87\xAA\xF0\x9F\x87\xB8'.decode() + ' Spanish',
        b'\xF0\x9F\x87\xAB\xF0\x9F\x87\xB7'.decode() + ' French',
        'Hebrew',
        b'\xF0\x9F\x87\xAE\xF0\x9F\x87\xB9'.decode() + ' Italian',
        b'\xF0\x9F\x87\xAF\xF0\x9F\x87\xB5'.decode() + ' Japanese',
        'Dutch',
        'Polish',
        'Portuguese',
        'Romanian',
        'Turkish',
        b'\xF0\x9F\x87\xA8\xF0\x9F\x87\xB3'.decode() + ' Chinese']


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Чтобы установить языки, нажмите сначала /from, затем /into")


@bot.message_handler(commands=['from'])
def from_(message):
    with shelve.open('languages') as languages:
        if str(message.chat.id) in languages.keys():
            languages[str(message.chat.id)] = [True, '', languages[str(message.chat.id)][2]]
        else:
            languages[str(message.chat.id)] = [True, '', '']
    keyboard = telebot.types.InlineKeyboardMarkup()
    for language in lang:
        keyboard.add(telebot.types.InlineKeyboardButton(text=language, callback_data=language.split()[-1].lower()))
    bot.send_message(chat_id=message.chat.id, text='Выберите язык из списка:', reply_markup=keyboard)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.message_handler(commands=['into'])
def into(message):
    with shelve.open('languages') as languages:
        if str(message.chat.id) in languages.keys():
            languages[str(message.chat.id)] = [False, languages[str(message.chat.id)][1], '']
        else:
            languages[str(message.chat.id)] = [False, '', '']
    keyboard = telebot.types.InlineKeyboardMarkup()
    for language in lang:
        keyboard.add(telebot.types.InlineKeyboardButton(text=language, callback_data=language.split()[-1].lower()))
    bot.send_message(chat_id=message.chat.id, text='Выберите язык из списка:', reply_markup=keyboard)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.message_handler(commands=['exchange'])
def exchange(message):
    with shelve.open('languages') as languages:
        if str(message.chat.id) in languages.keys():
            languages[str(message.chat.id)] = [True, languages[str(message.chat.id)][2], languages[str(message.chat.id)][1]]
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            print(languages[str(message.chat.id)])


@bot.message_handler(commands=['reset'])
def reset(message):
    with shelve.open('languages') as languages:
        languages[str(message.chat.id)] = [True, '', '']
        bot.send_message(chat_id=message.chat.id, text='Выберите языки.')
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.message_handler(commands=['selected'])
def selected(message):
    with shelve.open('languages') as languages:
        if str(message.chat.id) in list(languages.keys()):
            bot.send_message(chat_id=message.chat.id, text=f'Установлено: {languages[str(message.chat.id)][1]}-{languages[str(message.chat.id)][2]}')
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    with shelve.open('languages') as languages:
        if languages[str(call.message.chat.id)][0]:
            print(call.data)
            languages[str(call.message.chat.id)] = [True, call.data, languages[str(call.message.chat.id)][2]]
            bot.answer_callback_query(call.id, text=f'Вы успешно поменяли язык на {call.data}.')
            print(languages[str(call.message.chat.id)])
            bot.delete_message(call.message.chat.id, call.message.message_id)
        else:
            print(call.data)
            languages[str(call.message.chat.id)] = [False, languages[str(call.message.chat.id)][1], call.data]
            bot.answer_callback_query(call.id, text=f'Вы успешно поменяли язык на {call.data}.')
            print(languages[str(call.message.chat.id)])
            bot.delete_message(call.message.chat.id, call.message.message_id)



@bot.message_handler(content_types=['text'])
def send_text(message):
    with shelve.open('languages') as languages:
        if str(message.chat.id) in languages.keys() and '' not in languages:
            translate = translator(message.text, f'{languages[str(message.chat.id)][1]}-{languages[str(message.chat.id)][2]}')
            pos = 0
            while pos < len(translate[0]):
                bot.send_message(chat_id=message.chat.id, text=translate[0][pos:pos + 4097], parse_mode='Markdown')
                pos += 4097
            bot.send_message(chat_id=message.chat.id,
                             text=translate[1], parse_mode='Markdown')
        else:
            bot.send_message(chat_id=message.chat.id, text='Языки не выбраны.')


if __name__ == '__main__':
    bot.polling()


