import os
import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.environ.get('TELEGRAM_TOKEN')
API_KEY = os.environ.get('BRSAPI_KEY')

bot = telebot.TeleBot(TOKEN)

# گرفتن اطلاعات بازار
def get_full_data():
    url = f"https://brsapi.ir/Api/Market/Gold_Currency.php?key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    final_message = "نرخ بازار:\n" + "——————————————\n"

    sections = {
        "gold": "نرخ طلا و سکه",
        "currency": "نرخ ارز"
    }

    for key, title in sections.items():
        items = data.get(key, [])
        if items:
            final_message += f"\n{title}:\n"
            for item in items:
                name = item.get("name", "")
                unit = item.get("unit", "")
                price = item.get("price", "")
                change = item.get("change_value", "")
                percent = item.get("change_percent", "")
                line = f"{name}\nواحد: {unit} | قیمت: {price}\nتغییر: {change} | درصد: {percent}%\n"
                final_message += line + "------------------------\n"

    return final_message

# کیبورد با دکمه price
def main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("price"))
    return markup

# /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "سلام! برای دریافت نرخ طلا و ارز دکمه زیر را بزنید:",
        reply_markup=main_keyboard()
    )

# اگر دکمه price فشرده شد
@bot.message_handler(func=lambda message: message.text == "price")
def send_price(message):
    text = get_full_data()
    bot.send_message(message.chat.id, text)

# اجرای همیشگی ربات
bot.infinity_polling()
