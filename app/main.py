import telebot
from config import token
from bs4 import BeautifulSoup
import requests

bot = telebot.TeleBot(token)
print("Bot Started")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f"Hello. This is a bot that shows the weather forecast. Creator: @wuzi_10")


@bot.message_handler(func=lambda x: True)
def index(message):
    url = f"https://ua.sinoptik.ua/погода-{message.text}"
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    t = soup.find("p", class_="today-temp").get_text()
    time = soup.find("p", class_="today-time").get_text()
    descriptions = soup.findAll("div", class_="description")
    desc = ""
    for des in descriptions:
        desc += f'{des.text[1:]}\n'

    image = soup.find("div", class_="img").find('img')['src'][2:]
    infoDay = soup.find("div", class_="infoDaylight").get_text()[1:]
    infoVal = soup.find("p", class_="infoHistoryval").get_text()[1:]
    result = f"{time}\n\nТемпература: {t}\n\n{infoDay}\n\n{infoVal}\n\n{desc}"
    bot.send_photo(message.chat.id, image, caption=f"<b>{time}</b>\n\nТемпература: <b>{t}</b>\n\n{infoDay}\n\n{infoVal}\n\n{desc}", parse_mode="html")





bot.polling(non_stop=True)