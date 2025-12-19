import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# --- تنظیمات نهایی هوجت ---
BOT_TOKEN = '8231382550:AAEsU4F1Ph9H8GWWJd0ZJlYnhbhTNhA-NzI' 
GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbzuoHqfgucv_Ty5ePOlt7akh1lIMc2zQs3aIMFyrkKWMxCKIrPB_U-BQ9n-IYaab3m--Q/exec'
MINI_APP_URL = 'https://hojjataftab.github.io/Gimme5/' 

# تنظیمات لاگ برای مشاهده وضعیت در Render
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # بررسی آیدی دعوت‌کننده
    referrer_id = "DIRECT"
    if context.args:
        referrer_id = context.args[0]

    # ارسال اطلاعات به گوگل شیت
    user_data = {
        "uId": str(user.id),
        "username": user.username or user.first_name,
        "refBy": referrer_id
    }
    
    try:
        # ارسال درخواست به گوگل اسکریپت با زمان انتظار ۱۰ ثانیه
        requests.post(GOOGLE_SCRIPT_URL, json=user_data, timeout=10)
    except Exception as e:
        logging.error(f"Error connecting to Google Sheet: {e}")

    # متن پیام خوش‌آمدگویی
    welcome_text = (
        f"Hi {user.first_name}! ❄️\n\n"
        "Welcome to the **Gimme5 New Year Raffle**! 🎄\n\n"
        "Win **100 USDT** by just inviting 5 friends to our celebration.\n\n"
        "Tap the button below to check your progress and get your invite link! 👇"
    )

    # دکمه‌های شیشه‌ای
    keyboard = [
        [InlineKeyboardButton("🎁 OPEN GIMME5 APP", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/gemmi5bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

if __name__ == '__main__':
    # راه اندازی موتور ربات
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # فعال سازی دستور استارت
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    # شروع گوش دادن به پیام‌ها
    application.run_polling()
