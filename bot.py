import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

# এখানে আপনার BotFather থেকে পাওয়া টোকেনটি দিন
TOKEN = '8918160696:AAH2HalXDf0ddHyku9W8WmBdpH4HUToZyCY'
bot = telebot.TeleBot(TOKEN)

# ডেটা সেভ করার ফাংশন (কে কী করছে তা bot_log.txt ফাইলে লিখে রাখবে)
def log_activity(user_id, name, action):
    time_now = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    log_text = f"[{time_now}] {name} (ID: {user_id}) -> {action}\n"
    with open("bot_log.txt", "a", encoding="utf-8") as f:
        f.write(log_text)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    name = message.chat.first_name or "Unknown"
    
    # ইউজার বট স্টার্ট করলেই সেটি ফাইলে সেভ হয়ে যাবে
    log_activity(user_id, name, "বটে প্রবেশ করেছে (/start)")

    markup = InlineKeyboardMarkup(row_width=2)
    
    # URL এর বদলে callback_data ব্যবহার করা হয়েছে ট্র্যাকিং করার জন্য
    btn1 = InlineKeyboardButton("🎬 বাংলা ভিডিও", callback_data="bangla_video")
    btn2 = InlineKeyboardButton("🇬🇧 ইংরেজি", callback_data="english")
    btn3 = InlineKeyboardButton("💃 নাচ", callback_data="dance")
    btn4 = InlineKeyboardButton("🎵 গান", callback_data="song")
    btn5 = InlineKeyboardButton("💰 অনলাইন ইনকাম", callback_data="income")
    
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    bot.reply_to(message, "বটে স্বাগতম! আপনি কী দেখতে চান তা নিচের অপশনগুলো থেকে বেছে নিন:", reply_markup=markup)

# বাটন ক্লিকের রেসপন্স এবং ট্র্যাকিং করার অংশ
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user_id = call.message.chat.id
    name = call.message.chat.first_name or "Unknown"
    
    if call.data == "bangla_video":
        log_activity(user_id, name, "'বাংলা ভিডিও' অপশনে ক্লিক করেছে")
        bot.send_message(user_id, "🎬 বাংলা ভিডিওর লিংক: https://www.youtube.com/")
        
    elif call.data == "english":
        log_activity(user_id, name, "'ইংরেজি' অপশনে ক্লিক করেছে")
        bot.send_message(user_id, "🇬🇧 ইংরেজি ভিডিওর লিংক: https://www.youtube.com/")
        
    elif call.data == "dance":
        log_activity(user_id, name, "'নাচ' অপশনে ক্লিক করেছে")
        bot.send_message(user_id, "💃 নাচের ভিডিওর লিংক: https://www.youtube.com/")
        
    elif call.data == "song":
        log_activity(user_id, name, "'গান' অপশনে ক্লিক করেছে")
        bot.send_message(user_id, "🎵 গানের লিংক: https://www.youtube.com/")
        
    elif call.data == "income":
        log_activity(user_id, name, "'অনলাইন ইনকাম' অপশনে ক্লিক করেছে")
        bot.send_message(user_id, "💰 অনলাইন ইনকাম চ্যানেলের লিংক: https://t.me/telegram")
        
    # টেলিগ্রামকে বোঝানো যে ক্লিক রিসিভ হয়েছে (এতে বাটনের লোডিং আইকন থেমে যাবে)
    bot.answer_callback_query(call.id)

# আপনি এডমিন হিসেবে কে কে বট ব্যবহার করল তা দেখতে এই কমান্ডটি দেবেন
@bot.message_handler(commands=['log'])
def show_log(message):
    if os.path.exists("bot_log.txt"):
        with open("bot_log.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            # শুধু শেষের ২০ জনের ডেটা দেখাবে যাতে মেসেজ অনেক বড় না হয়ে যায়
            recent_logs = "".join(lines[-20:])
            bot.reply_to(message, f"📊 **বটের সর্বশেষ হিস্ট্রি:**\n\n{recent_logs}", parse_mode="Markdown")
    else:
        bot.reply_to(message, "এখনো কেউ আপনার বট ব্যবহার করেনি।")

print("Tracking Menu Bot is running...")
bot.polling()