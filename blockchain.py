import requests
from config import TON_API_KEY, TON_WALLET

def check_ton_payment(amount_expected, comment):
    url = f"https://toncenter.com/api/v2/getTransactions?address={TON_WALLET}&limit=10&api_key={TON_API_KEY}"
    try:
        data = requests.get(url).json()
        for tx in data.get("result", []):
            in_msg = tx.get("in_msg", {})
            incoming_value = int(in_msg.get("value", 0)) / 10**9
            tx_comment = in_msg.get("message", '').strip()
            if abs(incoming_value - amount_expected) < 0.0001 and tx_comment == comment:
                return True
        return False
    except Exception as e:
        print('Error checking payment:', e)
        return False
