from Token import TOKEN, keys
import telebot
from Extensions import CurrencyConverter, ConvertionException
#Телеграм канал бота
# t.me/CurrencySkillbot

bot = telebot.TeleBot(TOKEN)

# Приветственный message
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = f'Добро пожаловать,  {message.chat.username}! Чтобы начать работу, введите команду боту в следующем формате через пробел:\n    ' \
           f'Название валюты\n\
    в какую валюту конвертировать\n\
    Количество переводимой валюты\n\
    Например: Рубль Доллар 1\n\
    Список всех доступных валют можно увидеть, написав команду: /values'
    bot.reply_to(message, text)
# Список валют
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


# ввод вида валюты и вывод в консоль, запрашиваемый ответ, с текущей ценой онлайн
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров')
        quote, base, amount = values
        total_base = CurrencyConverter.getprice(quote, base, amount)
        result = float(total_base)*float(amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Неудалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {result} {base}'
        bot.send_message(message.chat.id, text)
bot.polling()