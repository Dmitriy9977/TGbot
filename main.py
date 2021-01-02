import telebot
from extensions import Parser, APIException
from config import TOKEN
import json

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    response_message = """Чтобы конвертировать валюту введите команды боту в следующем порядке:\n
<название валюты цену которой вы хотите узнать>
<название валюты в которой надо узнать цену первой валюты>
<количество первой валюты>\n
Пример конвертирование валюты:
доллар рубль 100 \n
Чтобы увидеть список доступных валют и правильность их написания для получения результата введите: /values
 """

    bot.send_message(message.chat.id, response_message)

@bot.message_handler(commands=['values'])
def start_message(message):
    values = Parser.get_currencys()
    response_message = []

    for i in values:
        response_message.append(f"{i} - {' '.join(values[i])}")

    bot.send_message(message.chat.id, '\n'.join(response_message) + "\n*Без учета регистра*")

@bot.message_handler(content_types=['text'])
def send_text(message):

    try:
        to_currency, from_currency, count = message.text.lower().split()
        response = Parser.get_price(to_currency.strip(), from_currency.strip(), count)
    except APIException as ex:
        bot.send_message(message.chat.id, ex.message)
    except ValueError:
        bot.send_message(message.chat.id, 'Неправильный ввод данных')
    except:
        bot.send_message(message.chat.id, 'Ошибка на сервере')
    else:
        response = json.loads(response)
        bot.send_message(message.chat.id, response['message'])

bot.polling()