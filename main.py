import os
import requests
import telebot
import arabic_reshaper
from bidi.algorithm import get_display

# گرفتن متغیرهای محیطی
TOKEN = os.environ.get('TELEGRAM_TOKEN')  # حواست باشه کلید درست رو استفاده کنی
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

    message = "نرخ بازار:\n——————————————\n"

    # فقط طلا و ارز نمایش داده شود
    sections = {
        "gold": "طلا و سکه",
        "currency": "ارز"
    }

    for key, title in sections.items():
        if key in data:
            message += f"\n{title}:\n"
            for item in data[key]:
                name = item.get('name', '')
                unit = item.get('unit', '')
                price = item.get('price', '')
                line = f"{name} | {unit} | قیمت: {price}"
                message += line + "\n"

    return fix(message)  # اصلاح فقط در انتها

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
