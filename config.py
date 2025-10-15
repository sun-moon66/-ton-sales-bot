import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
TON_WALLET = os.getenv("TON_WALLET")
TON_API_KEY = os.getenv("TON_API_KEY")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "30"))
