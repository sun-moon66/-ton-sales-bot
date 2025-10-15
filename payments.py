# =============================
# payments.py
# =============================
import urllib.parse

def generate_ton_link(wallet, amount, comment):
    """
    ساخت لینک پرداخت TON با فرمت ایمن و قابل استفاده در TON Keeper / Web
    """
    encoded_comment = urllib.parse.quote(str(comment))
    encoded_amount = str(amount)

    # لینک اصلی برای TON Keeper
    tonkeeper_link = f"tonkeeper://transfer/{wallet}?amount={encoded_amount}&text={encoded_comment}"

    # لینک رزرو برای مرورگر و کاربران بدون TON Keeper
    web_fallback = f"https://ton.app/pay?address={wallet}&amount={encoded_amount}&text={encoded_comment}"

    # ترکیب هر دو: با tonkeeper باز میشه و اگر مرورگره، fallback روی وب
    final_link = f"https://tonkeeper.com/transfer/{wallet}?amount={encoded_amount}&text={encoded_comment}"

    # برای ارسال در بات ترجیحاً از نسخه وب استفاده کن که در همه جا لود بشه
    return final_link
