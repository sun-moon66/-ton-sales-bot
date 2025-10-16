# =============================
# config.py
# =============================
import os
from dotenv import load_dotenv

load_dotenv()  # برای خواندن متغیرها هنگام تست محلی

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID") or 0)
TON_WALLET = os.getenv("TON_WALLET")  # آدرس Base64 برای لینک پرداخت tonkeeper.com
TON_WALLET_HEX = os.getenv("TON_WALLET_HEX")  # آدرس Hex ولت برای toncenter
TON_API_KEY = os.getenv("TON_API_KEY")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL") or 30)
