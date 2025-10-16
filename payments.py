# =============================
# payments.py
# =============================
import urllib.parse

def generate_ton_link(wallet, amount, comment):
    """
    ساخت لینک پرداخت TON که در تلگرام قابل کلیک باشد و Tonkeeper را باز کند
    """
    comment_encoded = urllib.parse.quote(comment)
    link = f"https://tonkeeper.com/transfer/{wallet}?amount={amount}&text={comment_encoded}"
    return link
