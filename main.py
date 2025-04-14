import os
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get('TELEGRAM_TOKEN')
API_KEY = os.environ.get('BRSAPI_KEY')

bot = telebot.TeleBot(TOKEN)

# گرفتن اطلاعات فقط برای بازار طلا و ارز
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

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("price", callback_data="get_price"))
    bot.send_message(message.chat.id, "سلام! برای دریافت نرخ طلا و ارز دکمه زیر را بزنید:", reply_markup=markup)

# وقتی روی دکمه کلیک می‌کنیم
@bot.callback_query_handler(func=lambda call: call.data == "get_price")
def callback_query(call):
    text = get_full_data()
    bot.send_message(call.message.chat.id, text)

# اجرای همیشگی ربات
bot.infinity_polling()
