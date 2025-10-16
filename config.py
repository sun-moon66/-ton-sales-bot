# =============================
# config.py
# =============================
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID") or 0)
TON_WALLET = os.getenv("TON_WALLET")  # فرم UQ... برای لینک پرداخت Tonkeeper
TON_WALLET_HEX = os.getenv("TON_WALLET_HEX")  # فرم 0:hex برای API toncenter.com
TON_API_KEY = os.getenv("TON_API_KEY")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL") or 30)
