import streamlit as st
import random
import datetime

# --- Theme Config ---
st.set_page_config(
    page_title="Bitcoin Wallet",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Constants ---
btc_price_usd = 68000
wallet_usd_balance = 900000
wallet_btc_balance = round(wallet_usd_balance / btc_price_usd, 8)
wallet_address = f"bc1q{random.randint(10**10, 10**11 - 1)}wallet"

# --- Helper Functions ---
def generate_transactions(num=6):
    transactions = []
    for _ in range(num):
        amount = round(random.uniform(0.01, 0.25), 6)
        tx_type = random.choice(["Received", "Sent"])
        date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 20))
        tx = {
            "type": tx_type,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Confirmed" if tx_type == "Received" else "Pending",
            "tx_hash": f"0x{random.randint(10**15, 10**16 - 1):x}"
        }
        transactions.append(tx)
    return transactions

# --- Dark Mode CSS ---
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stApp {
        background-color: #0e1117;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- UI ---
st.title("🪙 Bitcoin Wallet")

st.subheader("📬 Wallet Address")
st.code(wallet_address)

st.metric("💰 BTC Balance", f"{wallet_btc_balance} BTC")
st.metric("💵 USD Equivalent", f"${wallet_usd_balance:,.2f}")

# --- Send BTC Interface ---
st.subheader("📤 Send Bitcoin")

with st.form("send_btc_form"):
    recipient = st.text_input("Recipient BTC Address")
    amount_to_send = st.number_input("Amount to Send (BTC)", min_value=0.0001, max_value=wallet_btc_balance)
    submitted = st.form_submit_button("Send")

    if submitted:
        if recipient and amount_to_send <= wallet_btc_balance:
            st.success(f"✅ {amount_to_send} BTC sent to {recipient}")
        else:
            st.error("❌ Invalid address or amount exceeds wallet balance.")

# --- Transactions ---
st.subheader("📄 Recent Transactions")
transactions = generate_transactions()

for tx in transactions:
    st.markdown(f"""
    **{tx['type']}** | `{tx['date']}`  
    Amount: `{tx['amount']} BTC`  
    Status: **{tx['status']}**  
    Tx Hash: `{tx['tx_hash']}`  
    ---
    """)
