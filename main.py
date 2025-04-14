import os
import requests
import telebot
import arabic_reshaper
from bidi.algorithm import get_display

# گرفتن توکن‌ها از محیط
TOKEN = os.environ.get('TELEGRAM_TOKEN')
API_KEY = os.environ.get('BRSAPI_KEY')

bot = telebot.TeleBot(TOKEN)

# اصلاح فقط متن فارسی خالص
def fix(text):
    return get_display(arabic_reshaper.reshape(str(text)))

# گرفتن اطلاعات از API و ساخت پیام کامل
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
            final_message += f"\n{fix(title)}:\n"
            for item in items:
                name = fix(item.get("name", ""))
                unit = item.get("unit", "")
                price = item.get("price", "")
                change = item.get("change_value", "")
                percent = item.get("change_percent", "")

                # فقط نام فارسی راست‌چین شه
                final_message += f"{name}\nواحد: {unit} | قیمت: {price}\nتغییر: {change} | درصد: {percent}%\n"
                final_message += "------------------------\n"

    return final_message

# شروع بات
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, fix("سلام! برای دریافت نرخ طلا و ارز، دستور /price را ارسال کنید."))

# ارسال نرخ بازار
@bot.message_handler(commands=['price'])
def send_price(message):
    text = get_full_data()
    bot.send_message(message.chat.id, text)

# اجرای همیشگی ربات
bot.infinity_polling()
