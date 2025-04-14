import os
import requests
import telebot
import arabic_reshaper
from bidi.algorithm import get_display

# گرفتن متغیرهای محیطی
TOKEN = os.environ.get('TELEGRAM_TOKEN')
API_KEY = os.environ.get('BRSAPI_KEY')

bot = telebot.TeleBot(TOKEN)

# اصلاح متن فارسی برای راست‌چین شدن
def fix(text):
    return get_display(arabic_reshaper.reshape(str(text)))

# گرفتن اطلاعات از API و ساخت پیام کامل
def get_full_data():
    url = f"https://brsapi.ir/Api/Market/Gold_Currency.php?key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    final_message = fix("نرخ بازار:\n") + "——————————————\n"

    # فقط طلا و ارز نمایش داده شود
    sections = {
        "gold": "طلا و سکه",
        "currency": "ارز"
    }

    for key, title in sections.items():
        if key in data:
            final_message += fix(f"\n{title}:\n")
            for item in data[key]:
                name = fix(item.get('name', ''))
                unit = fix(item.get('unit', ''))
                price = fix(item.get('price', ''))
                line = f"{name} | {unit} | قیمت: {price}"
                final_message += line + "\n"

    return final_message

# /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, fix("سلام! برای دریافت نرخ بازار دستور /price را ارسال کنید."))

# /price
@bot.message_handler(commands=['price'])
def send_price(message):
    try:
        text = get_full_data()
        bot.send_message(message.chat.id, text)
    except Exception as e:
        bot.send_message(message.chat.id, fix("خطایی رخ داده است."))

# اجرای ربات
bot.infinity_polling()
