def generate_ton_link(wallet, amount, comment):
    link = f"https://tonhub.com/transfer/{wallet}?amount={amount}&text={comment}"
    return link
