import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# --- تنظیمات شما ---
BOT_TOKEN = 'توکن_ربات_شما' # توکنی که از BotFather گرفتی
GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbzuoHqfgucv_Ty5ePOlt7akh1lIMc2zQs3aIMFyrkKWMxCKIrPB_U-BQ9n-IYaab3m--Q/exec'
MINI_APP_URL = 'https://hojjataftab.github.io/Gimme5/' 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    referrer_id = "DIRECT"
    if context.args:
        referrer_id = context.args[0]

    # ثبت در گوگل شیت
    user_data = {
        "uId": str(user.id),
        "username": user.username or user.first_name,
        "refBy": referrer_id
    }
    try:
        requests.post(GOOGLE_SCRIPT_URL, json=user_data)
    except:
        pass

    welcome_text = (
        f"Hi {user.first_name}! ❄️\n\n"
        "Welcome to **Gimme5 New Year Raffle**! 🎄\n\n"
        "Win **100 USDT** by inviting 5 friends.\n\n"
        "Tap below to check your status! 👇"
    )

    keyboard = [
        [InlineKeyboardButton("🎁 OPEN GIMME5 APP", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/gemmi5bot")]
    ]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.run_polling()
