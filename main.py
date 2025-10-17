# =============================
# main.py (Final – Render Free Safe Version)
# =============================
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask
import asyncio, threading, time, nest_asyncio

from config import *
from payments import generate_ton_link
from blockchain import check_ton_payment

# اجازه اجرای چندبخشی asyncio در محیط‌های درحال‌اجرا (مثل Flask)
nest_asyncio.apply()

# -----------------------------
# Keepalive Flask برای Render free plan
# -----------------------------
def keep_alive():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "✅ Ton Sales Bot running on Render free plan!"

    # اجرای Flask در Thread اصلی (Render انتظار همین رفتار را دارد)
    app.run(host="0.0.0.0", port=10000)

# -----------------------------
# محصولات تستی
# -----------------------------
PRODUCTS = [
    {"id": 1, "name": "نرم‌افزار تستی", "price": 0.5, "file": "https://example.com/file1.zip"},
    {"id": 2, "name": "بازی اندروید", "price": 0.8, "file": "https://example.com/game.apk"},
]

# -----------------------------
# هندلرهای تلگرام
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton(p["name"], callback_data=f"buy_{p['id']}")] for p in PRODUCTS]
    msg = "به فروشگاه TON خوش اومدی 🌐\nیک محصول انتخاب کن:"
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(buttons))

async def buy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    pid = int(query.data.replace("buy_", ""))
    p = next(item for item in PRODUCTS if item["id"] == pid)
    comment = f"ORDER{pid}_{int(time.time())}"
    link = generate_ton_link(TON_WALLET, p["price"], comment)

    await query.message.reply_text(
        f"💰 مبلغ: {p['price']} TON\n📦 محصول: {p['name']}\n\n"
        f"برای پرداخت روی لینک زیر بزن:\n{link}\n\nبعد از پرداخت تا تأیید صبر کن..."
    )

    # بررسی متناوب پرداخت
    for _ in range(10):
        await asyncio.sleep(CHECK_INTERVAL)
        if check_ton_payment(p["price"], comment):
            await query.message.reply_text(f"✅ پرداخت تأیید شد!\n📁 لینک دانلود:\n{p['file']}")
            if ADMIN_ID:
                await context.bot.send_message(
                    ADMIN_ID, f"💸 خرید جدید: {p['name']} ({p['price']} TON)"
                )
            return
    await query.message.reply_text("❌ پرداخت پیدا نشد، بعداً دوباره امتحان کن.")

# -----------------------------
# اجرای همزمان Flask و Bot
# -----------------------------
def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buy_handler, pattern="^buy_"))

    print("🚀 Bot polling started on Render free plan...")
    app.run_polling(stop_signals=None)

if __name__ == "__main__":
    # اجرای ربات در Thread جدا و Flask در Thread اصلی
    threading.Thread(target=start_bot, daemon=True).start()
    keep_alive()
