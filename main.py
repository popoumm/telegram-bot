import requests
import telebot

TOKEN = '7649717713:AAEUUoAsrzsPgQ7LHPLXUxoW_oJ2079JYa8'
bot = telebot.TeleBot(TOKEN)

# گرفتن اطلاعات فقط برای بازار طلا و ارز
def get_full_data():
    url = "https://brsapi.ir/Api/Market/Gold_Currency.php?key=FreeaWKXMvkIa3k7ZNUobmPrX1hJfcUG"
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

# شروع بات
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! برای دریافت نرخ طلا و ارز، دستور /price را ارسال کنید.")

# ارسال نرخ بازار
@bot.message_handler(commands=['price'])
def send_price(message):
    text = get_full_data()
    bot.send_message(message.chat.id, text)

# اجرای همیشگی ربات
bot.infinity_polling()