Lucky, [Dec 30, 2025 at 19:15]
import telebot
import json
import os

# --- 1. الإعدادات ---
API_TOKEN = '8295490040:AAFd4-C8W4INEWcUO--toIOnQRFbOD786Es'
bot = telebot.TeleBot(API_TOKEN)

BOSS_IDS = [5218996367]
YOUR_USERNAME = "@LuckyQR9"

BASE_DIR = os.path.dirname(os.path.abspath(file))
DB_FILE = os.path.join(BASE_DIR, "scammers_data.json")

# --- 2. نظام قاعدة البيانات (Persistent Storage) ---
def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return {}
    return {}

def save_data(data):
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except: pass

scammers_advanced_db = load_data()

# --- 3. القائمة الرئيسية (Dual Language Buttons) ---
def show_main_menu(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton("🔍 Check Player / Проверить игрока", callback_data="check_user"),
        telebot.types.InlineKeyboardButton("🛡️ Safety Guide / Гайд по безопасности", callback_data="safety_guide"),
        telebot.types.InlineKeyboardButton("🤝 Middleman / Гарант", callback_data="req_mid"),
        telebot.types.InlineKeyboardButton("📢 Report Scam / Пожаловаться", callback_data="report_scam")
    )
    text = "⬇️ Choose an option / Выберите вариант:"
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')

# --- 4. معالج البداية (Dual Language Welcome) ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if user_id in BOSS_IDS:
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            telebot.types.InlineKeyboardButton("🖼️ إضافة نصاب", callback_data="post_scammer"),
            telebot.types.InlineKeyboardButton("📋 عرض القائمة", callback_data="view_list"),
            telebot.types.InlineKeyboardButton("❌ إزالة نصاب", callback_data="rem_scammer")
        )
        bot.send_message(user_id, f"👑 أهلاً يا زعيم {YOUR_USERNAME}!", reply_markup=markup)
    else:
        welcome_txt = (
            "🛡️ Oxide Guardian Bot\n\n"
            "🇬🇧 Welcome! Use this bot to check scammers or report them.\n"
            "🇷🇺 Добро пожаловать! Используйте этого бота, чтобы проверить мошенников или сообщить о них."
        )
        bot.send_message(message.chat.id, welcome_txt, parse_mode='Markdown')
        show_main_menu(message)

# --- 5. معالج الأزرار (Dual Language Responses) ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id

    if call.data == "view_list" and user_id in BOSS_IDS:
        names = list(scammers_advanced_db.keys())
        res = "📋 قائمة النصابين:\n• " + "\n• ".join(names) if names else "القائمة فارغة."
        bot.send_message(user_id, res)

    elif call.data == "check_user":
        txt = "🔍 Enter Player ID or Username:\n🔍 Введите ID игрока или имя пользователя:"
        msg = bot.send_message(user_id, txt, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_advanced_check)

    elif call.data == "safety_guide":
        guide = (
            "🛡️ Safety Rules / Правила безопасности:\n\n"
            "🇬🇧 1. Never trade without a trusted middleman.\n"
            "🇷🇺 1. Никогда не торгуйте без проверенного гаранта.\n\n"
            "🇬🇧 2. Always check the player ID here first.\n"
            "🇷🇺 2. Всегда сначала проверяйте ID игрока здесь.\n\n"
            "🇬🇧 3. Record a video of every trade.\n"
            "🇷🇺 3. Записывайте видео каждой сделки."
        )
        bot.send_message(user_id, guide, parse_mode='Markdown')
        show_main_menu(call.message)
Lucky, [Dec 30, 2025 at 19:15]
elif call.data == "report_scam":
        txt = "⚠️ Send proof (Screenshots/Details):\n⚠️ Пришлите доказательства (Скриншоты/Детали):"
        msg = bot.send_message(user_id, txt, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_report)

    elif call.data == "req_mid":
        bot.send_message(user_id, f"🤝 Admin / Админ: {YOUR_USERNAME}")
        show_main_menu(call.message)

    elif call.data == "post_scammer" and user_id in BOSS_IDS:
        msg = bot.send_message(user_id, "🖼️ أرسل صورة الدليل:")
        bot.register_next_step_handler(msg, get_scammer_photo)

    elif call.data == "rem_scammer" and user_id in BOSS_IDS:
        msg = bot.send_message(user_id, "🗑️ أرسل الاسم لحذفه:")
        bot.register_next_step_handler(msg, process_remove)

    bot.answer_callback_query(call.id)

# --- 6. الوظائف المنطقية ---
def process_advanced_check(message):
    name = message.text.replace("@", "").strip() if message.text else ""
    if name in scammers_advanced_db:
        data = scammers_advanced_db[name]
        caption = (
            f"🔴 SCAMMER ALERT! / ВНИМАНИЕ МОШЕННИК!\n\n"
            f"📝 Details / Детали: {data['details']}"
        )
        bot.send_photo(message.chat.id, data['photo'], caption=caption, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "🟢 CLEAN PLAYER / ЧИСТЫЙ ИГРОК")
    show_main_menu(message)

def process_report(message):
    for boss in BOSS_IDS:
        if message.content_type == 'photo':
            bot.send_photo(boss, message.photo[-1].file_id, caption=f"📩 بلاغ جديد من {message.from_user.id}")
        else:
            bot.send_message(boss, f"📩 بلاغ جديد من {message.from_user.id}:\n{message.text}")
    bot.send_message(message.chat.id, "✅ Sent! / Отправлено!")
    show_main_menu(message)

# --- وظائف الإدارة (Admin Functions) ---
def get_scammer_photo(message):
    if message.content_type == 'photo':
        photo_id = message.photo[-1].file_id
        msg = bot.send_message(message.chat.id, "✅ أرسل الاسم (ID/User):")
        bot.register_next_step_handler(msg, get_scammer_name, photo_id)
    else:
        bot.send_message(message.chat.id, "❌ أرسل صورة!")

def get_scammer_name(message, photo_id):
    name = message.text.replace("@", "").strip()
    msg = bot.send_message(message.chat.id, "✅ أرسل تفاصيل النصب:")
    bot.register_next_step_handler(msg, finish_scammer_entry, photo_id, name)

def finish_scammer_entry(message, photo_id, name):
    scammers_advanced_db[name] = {'photo': photo_id, 'details': message.text}
    save_data(scammers_advanced_db)
    bot.send_message(message.chat.id, f"✅ تم الحفظ بنجاح: {name}")

def process_remove(message):
    name = message.text.replace("@", "").strip()
    if name in scammers_advanced_db:
        del scammers_advanced_db[name]
        save_data(scammers_advanced_db)
        bot.send_message(message.chat.id, f"🗑️ تم حذف {name}")
    else:
        bot.send_message(message.chat.id, "❌ غير موجود")

print("✅ Bilingual Bot is Online!")
bot.infinity_polling()
