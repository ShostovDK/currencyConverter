import telebot
from tok import key
from telebot import types
import requests

cash = 0
bot = telebot.TeleBot(key)


@bot.message_handler(commands=['start'])
def func(message):
    bot.send_message(message.chat.id, "Здравствуйте! Введите сумму")
    bot.register_next_step_handler(message, func2)


def func2(message):
    global cash
    try:
        cash = float(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Hеверный формат")
        return
    if cash > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("USD/EUR", callback_data="usd/eur")
        btn2 = types.InlineKeyboardButton("EUR/USD", callback_data="eur/usd")
        btn3 = types.InlineKeyboardButton("USD/GBP", callback_data="usd/gbp")
        btn4 = types.InlineKeyboardButton("Дpyroe", callback_data="else")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Bыбeрите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Введите число больше 0')
        bot.register_next_step_handler(message, func2)


@bot.callback_query_handler(func=lambda call: True)
def callback_message(call):
    if call.data != 'else':
        val = call.data.upper().split('/')
        url = f'https://v6.exchangerate-api.com/v6/436fa9ab7cb5fffb88609beb/pair/{val[0]}/{val[1]}'
        response = requests.get(url)
        data = response.json()
        rate = data['conversion_rate']
        res = cash * rate
        bot.send_message(call.message.chat.id, f'{cash} {val[0]} is {round(res, 2)} {val[1]}')
        bot.register_next_step_handler(call.message, func2)
    else:
        bot.send_message(call.message.chat.id, f'Введите пару значений.')
        bot.register_next_step_handler(call.message, my_cur)


def my_cur(message):
    val = message.text.upper().split('/')
    url = f'https://v6.exchangerate-api.com/v6/436fa9ab7cb5fffb88609beb/pair/{val[0]}/{val[1]}'
    response = requests.get(url)
    data = response.json()
    rate = data['conversion_rate']
    res = cash * rate
    bot.send_message(message.chat.id, f'{cash} {val[0]} is {round(res, 2)} {val[1]}')
    bot.register_next_step_handler(message, func2)


bot.polling()

