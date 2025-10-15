import asyncio, time, json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from config import *
from payments import generate_ton_link
from blockchain import check_ton_payment

# خواندن محصولات از JSON
def load_products():
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = load_products()
    if not products:
        await update.message.reply_text('⛔️ هیچ محصولی در دسترس نیست.')
        return

    buttons = [[InlineKeyboardButton(p['name'], callback_data=f"buy_{p['id']}")] for p in products]
    await update.message.reply_text('به فروشگاه TON خوش اومدی 🌐
یک محصول انتخاب کن:',
                                    reply_markup=InlineKeyboardMarkup(buttons))

async def buy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pid = int(query.data.replace('buy_', ''))
    product = next(p for p in load_products() if p['id'] == pid)

    comment = f"ORDER{pid}_{int(time.time())}"
    link = generate_ton_link(TON_WALLET, product['price'], comment)

    await query.message.reply_text(
        f"💰 مبلغ: {product['price']} TON
"
        f"📦 محصول: {product['name']}

"
        f"برای پرداخت روی لینک زیر بزن:
{link}

"
        "بعد از پرداخت، چند لحظه صبر کن تا تأیید بشه..."
    )

    for _ in range(10):
        await asyncio.sleep(CHECK_INTERVAL)
        if check_ton_payment(product['price'], comment):
            await query.message.reply_text(
                f"✅ پرداخت تأیید شد!
رمز فایل: {product['password']}"
            )
            if ADMIN_ID:
                await context.bot.send_message(ADMIN_ID, f"💸 خرید جدید: {product['name']} ({product['price']} TON)")
            return

    await query.message.reply_text('❌ پرداخت پیدا نشد. اگه پرداخت کردی، چند دقیقه بعد دوباره امتحان کن.')

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(buy_handler, pattern='^buy_'))
    print('Bot running...')
    app.run_polling()

if __name__ == '__main__':
    main()
