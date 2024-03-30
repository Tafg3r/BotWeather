import telebot
from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.exceptions import NotFoundError

bot = telebot.TeleBot("Your token here") # important moment 1

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Добро пожаловать, ' + str(message.from_user.first_name) + ',\n/start - запуск бота\n/help - команды бота\nЧтобы узнать погоду напишите в чат название города')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '/start - запуск бота\n/help - команды бота\nЧтобы узнать погоду напишите в чат название города')

@bot.message_handler(content_types=['text'])
def test(message):
    try:
        place = message.text

        config_dict = get_default_config()
        config_dict['language'] = 'ru'              # your language setting

        owm = OWM('Token by website', config_dict)  # important moment 2
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(place)
        w = observation.weather

        t = w.temperature("celsius")
        t1 = t['temp']
        t2 = t['feels_like']
        t3 = t['temp_max']
        t4 = t['temp_min']

        wi = w.wind()['speed']
        dt = w.detailed_status

        bot.send_message(message.chat.id, "В городе " + str(place) + " температура:   " + str(t1) + " °C" + "\n" +
                        "Максимальная температура:   " + str(t3) + " °C" +"\n" +
                        "Минимальная температура:   " + str(t4) + " °C" + "\n" +
                        "Ощущается как:   " + str(t2) + " °C" + "\n" +
                        "Скорость ветра:   " + str(wi) + " м/с" + "\n" +
                        "Описание:   " + str(dt))

    except NotFoundError:
        bot.send_message(message.chat.id,"Такой город не найден!")
        print(str(message.text),"- не найден")

    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при обработке запроса.")
        print("Error:", e)

bot.polling(none_stop=True, interval=0)