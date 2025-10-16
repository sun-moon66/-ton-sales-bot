# =============================
# blockchain.py
# =============================
import requests
from config import TON_API_KEY, TON_WALLET_HEX

def check_ton_payment(amount_expected, comment):
    """
    بررسی آخرین تراکنش‌های کیف پول TON و تطبیق مبلغ و توضیح (Comment)
    """
    url = f"https://toncenter.com/api/v2/getTransactions?address={TON_WALLET_HEX}&limit=10&api_key={TON_API_KEY}"
    try:
        data = requests.get(url).json()
        txs = data.get("result", [])
        for tx in txs:
            in_msg = tx.get("in_msg", {})
            value = int(in_msg.get("value", 0)) / 10**9
            msg = in_msg.get("message", "").strip()
            if abs(value - amount_expected) < 0.0001 and msg == comment:
                return True
        return False
    except Exception as e:
        print("Error checking payment:", e)
        return False
