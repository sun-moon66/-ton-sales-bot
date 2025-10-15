# =============================
# main.py — فروش رمز ZIP از طریق TON
# =============================
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio, json, time
from config import *
from payments import generate_ton_link
from blockchain import check_ton_payment

# خواندن محصولات از فایل JSON
def load_products():
    try:
        with open("products.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("خطا در خواندن products.json:", e)
        return []

PRODUCTS = load_products()


# =============================
# /start — نمایش لیست محصولات
# =============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not PRODUCTS:
        await update.message.reply_text("هیچ محصولی ثبت نشده.")
        return
    buttons = [[InlineKeyboardButton(p["name"], callback_data=f"buy_{p['id']}")] for p in PRODUCTS]
    await update.message.reply_text(
        "🛒 فایل زیپ مورد نظرت رو از کانال بگیر و برای دریافت رمزش یکی از گزینه‌های زیر رو انتخاب کن 👇",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# =============================
# هندل خرید و بررسی پرداخت TON
# =============================
async def buy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pid = int(query.data.replace("buy_", ""))
    product = next((p for p in PRODUCTS if p["id"] == pid), None)
    if not product:
        await query.message.reply_text("❌ محصول یافت نشد.")
        return

    comment = f"ORDER{pid}_{int(time.time())}"
    pay_link = generate_ton_link(TON_WALLET, product["price"], comment)

    await query.message.reply_text(
        f"📦 {product['name']}\n💰 مبلغ: {product['price']} TON\n\n"
        "برای پرداخت TON روی لینک زیر بزن 👇\n"
        f"{pay_link}\n\n"
        "بعد از پرداخت، چند لحظه صبر کن تا تأیید بشه..."
    )

    for _ in range(10):
        await asyncio.sleep(CHECK_INTERVAL)
        if check_ton_payment(product["price"], comment):
            await query.message.reply_text(
                f"✅ پرداخت تأیید شد!\n"
                f"📦 {product['name']}\n"
                f"🔑 رمز فایل: `{product['password']}`",
                parse_mode="Markdown"
            )
            if ADMIN_ID:
                await context.bot.send_message(
                    ADMIN_ID,
                    f"💸 خرید: {product['name']} — {product['price']} TON"
                )
            return

    await query.message.reply_text("❌ پرداخت پیدا نشد. اگر پرداخت کردی، بعد از چند دقیقه دوباره امتحان کن.")

# =============================
# اجرای ربات
# =============================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buy_handler, pattern="^buy_"))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
