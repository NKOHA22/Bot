import telebot
from telebot import types
import requests
from datetime import datetime

TOKEN = '5610003390:AAGGunP3At0xVPgkw9QPvvC7WpqWZ0EkGkA'
open_weather_token = "5afee5cf78163a047aa882e3d63fbf5f"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('💵Курсы валют')
    item2 = types.KeyboardButton('⛅️Погода')
    item3 = types.KeyboardButton('📰Новости')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Привет,{0.first_name}!👋".format(
        message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):

    if message.chat.type == 'private':

        if message.text == '💵Курсы валют':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Курс Доллара')
            item2 = types.KeyboardButton('Курс Евро')
            item3 = types.KeyboardButton('Курс Рубля')
            item4 = types.KeyboardButton('Курс Юаня')
            back = types.KeyboardButton('🔙Назад')
            markup.add(item1, item2, item3, item4, back)
            bot.send_message(message.chat.id, "{0.first_name}, вы открыли раздел «💵Курсы валют»!".format(message.from_user),
                             reply_markup=markup)

        elif message.text == '⛅️Погода':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton(
                'Посмотреть погоду', callback_data="0")
            back = types.InlineKeyboardButton('🔙Назад', callback_data="1")
            markup.add(item1, back)
            bot.send_message(message.chat.id, "{0.first_name}, вы открыли раздел «⛅️Погода»!".format(message.from_user),
                             reply_markup=markup)

            @bot.callback_query_handler(func=lambda call: True)
            def weather_answer(call):
                if call.message:
                    if call.data == '0':
                        bot.reply_to(
                            call.message, "🌇Введите название города:")
                        bot.register_next_step_handler(
                            message, callback=showWeather)

            def get_weather(city):

                base_url = "https://api.openweathermap.org/data/2.5/weather?&units=metric"
                url = base_url + "&appid=" + open_weather_token + "&q=" + city
                response = requests.get(url)
                data = response.json()
                return data

            def showWeather(message):

                code_to_emoji = {
                    "Clear": "Ясно U+2600",
                    "Clouds": "Облачно U+1F325",
                    "Rain": "Дождь U+1F327",
                    "Drizzle": "Дождь U+2614",
                    "Thunderstorm": "Гроза U+1F329",
                    "Snow": "Снег U+2744",
                    "Mist": "Туман U+1F32B"
                }

                city = message.text
                print(city)
                data = get_weather(city)

                weather_description = data["weather"][0]["main"]

                if weather_description in code_to_emoji:
                    wd = code_to_emoji[weather_description]

                wd = "Посмотри в окно, мб там апокалипсис. А я просто бот🤖"

                x = data["main"]
                y = data["wind"]
                z = data["sys"]
                cur_temperature = round(x["temp"])
                cur_humidity = x["humidity"]
                cur_pressure = x["pressure"]
                cur_wind = y["speed"]
                sunrise_timestamp = datetime.fromtimestamp(z["sunrise"])
                sunset_timestamp = datetime.fromtimestamp(z["sunset"])
                text = (f"***{datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                        f"Погода в городе: {city}\nТемпература: {cur_temperature}°C {wd}\n"
                        f"Влажность: {cur_humidity}%\nДавление: {cur_pressure} мм.рт.ст\n"
                        f"Скорость ветра: {cur_wind}км/ч\nВосход: {sunrise_timestamp}\nЗакат: {sunset_timestamp}\n"
                        f"***Хорошего дня и удачи!***")
                bot.send_message(message.chat.id, text, parse_mode='Markdown')
                # bot.reply_to(message, str(
                #     text), reply_markup=markup)

                if message != city:
                    bot.send_message(
                        message.chat.id, "Не нашел информации по вашему запросу😭")

        elif message.text == '📰Новости':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('🇰🇿 Новости Казахстана')
            item2 = types.KeyboardButton('🌎Новости Мира')
            back = types.KeyboardButton('🔙Назад')
            markup.add(item1, item2, back)

            bot.send_message(message.chat.id, "{0.first_name}, вы открыли раздел «📰Новости»!".format(message.from_user),
                             reply_markup=markup)

        elif message.text == '🌎Новости Мира':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton('🔙Назад')
            markup.add(back)
            bot.send_message(message.chat.id,
                             "{0.first_name},вы открыли раздел «🌎Новости Мира»!".format(
                                 message.from_user),
                             reply_markup=markup)

        elif message.text == '🇰🇿 Новости Казахстана':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            bot.send_message(message.chat.id,
                             "{0.first_name},вы открыли раздел «🇰🇿 Новости Казахстана»!".format(
                                 message.from_user),
                             reply_markup=markup)

        elif message.text == '🔙Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('💵Курсы валют')
            item2 = types.KeyboardButton('⛅️Погода')
            item3 = types.KeyboardButton('📰Новости')
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, "Привет,{0.first_name}!👋".format(
                message.from_user), reply_markup=markup)

        else:
            bot.send_message(
                message.chat.id, 'Я тебя не понимаю. Напиши /help.')


bot.polling(non_stop=True)
