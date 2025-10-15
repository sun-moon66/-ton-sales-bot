# =============================
# payments.py
# =============================
import urllib.parse

def generate_ton_link(wallet, amount, comment):
    """
    ساخت لینک پرداخت TON که مستقیماً در اپ Tonkeeper باز شود
    """
    comment_encoded = urllib.parse.quote(comment)
    link = f"tonkeeper://transfer/{wallet}?amount={amount}&text={comment_encoded}"
    return link
