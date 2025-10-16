# =============================
# main.py (Render Free + PTB 21 compatible)
# =============================
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from flask import Flask
import asyncio, threading, time

from config import *
from payments import generate_ton_link
from blockchain import check_ton_payment

# ----------------------------- 
# Keepalive (Flask on port 10000)
# -----------------------------
def keep_alive():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "✅ Ton Sales Bot running on Render free plan!"
    app.run(host="0.0.0.0", port=10000)

thread = threading.Thread(target=keep_alive)
thread.daemon = True
thread.start()
# -----------------------------

PRODUCTS = [
    {"id": 1, "name": "نرم‌افزار تستی", "price": 0.5, "file": "https://example.com/file1.zip"},
    {"id": 2, "name": "بازی اندروید", "price": 0.8, "file": "https://example.com/game.apk"},
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton(p["name"], callback_data=f"buy_{p['id']}")] for p in PRODUCTS]
    text = "به فروشگاه TON خوش اومدی 🌐\nیکی از محصولات زیر رو انتخاب کن:"
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

async def buy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pid = int(query.data.replace("buy_", ""))
    product = next(p for p in PRODUCTS if p["id"] == pid)
    comment = f"ORDER{pid}_{int(time.time())}"
    pay_link = generate_ton_link(TON_WALLET, product["price"], comment)
    msg = (
        f"💰 مبلغ: {product['price']} TON\n"
        f"📦 محصول: {product['name']}\n\n"
        f"برای پرداخت روی لینک زیر بزن:\n{pay_link}\n\n"
        "⏳ بعد از پرداخت، تا تأیید صبر کن..."
    )
    await query.message.reply_text(msg)

    for _ in range(10):
        await asyncio.sleep(CHECK_INTERVAL)
        if check_ton_payment(product["price"], comment):
            await query.message.reply_text(f"✅ پرداخت تأیید شد!\n📁 لینک دانلود:\n{product['file']}")
            if ADMIN_ID:
                await context.bot.send_message(ADMIN_ID, f"💸 خرید جدید: {product['name']} ({product['price']} TON)")
            return
    await query.message.reply_text("❌ پرداخت پیدا نشد. اگر پرداخت کردی، چند دقیقه بعد امتحان کن.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buy_handler, pattern="^buy_"))

    print("🚀 Bot running on Render (Free Plan + Python 3.13 compatible)")
    await app.run_polling(close_loop=False)

if __name__ == "__main__":
    asyncio.run(main())
