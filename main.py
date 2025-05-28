import streamlit as st
import random
import datetime

# --- CONFIGURATION ---
OWNER_NAME = "Jaspal Birdi Singh"
btc_price_usd = 68000
wallet_usd_balance = 900000
wallet_btc_balance = round(wallet_usd_balance / btc_price_usd, 8)
wallet_address = "18zW9ngXygR4BmNHk8vFVzybAUq7Y9LVkY"

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Bitcoin Wallet",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- DARK MODE STYLE ---
st.markdown("""
    <style>
        body, .stApp {
            background-color: #0e1117;
            color: white;
        }
        .block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- TRANSACTION GENERATOR WITH DESCRIPTION ---
def generate_transactions(num=6):
    transactions = []

    # Main deposit transaction with description
    initial_tx = {
        "type": "Received",
        "amount": round(wallet_usd_balance / btc_price_usd, 8),
        "date": "2025-05-30 10:00:00",
        "status": "Confirmed",
        "tx_hash": f"0x{random.randint(10**15, 10**16 - 1):x}",
        "description": "Publishers Clearing House"
    }
    transactions.append(initial_tx)

    for _ in range(num):
        amount = round(random.uniform(0.01, 0.25), 6)
        tx_type = random.choice(["Received", "Sent"])
        date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 20))
        tx = {
            "type": tx_type,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Confirmed" if tx_type == "Received" else "Pending",
            "tx_hash": f"0x{random.randint(10**15, 10**16 - 1):x}",
            "description": ""
        }
        transactions.append(tx)

    return transactions

# --- HEADER ---
st.title("🪙 Bitcoin Wallet Dashboard")
st.caption(f"Wallet Owner: **{OWNER_NAME}**")

# --- WALLET INFO ---
st.subheader("📬 Wallet Address")
st.code(wallet_address, language="")

col1, col2 = st.columns(2)
col1.metric("💰 BTC Balance", f"{wallet_btc_balance} BTC")
col2.metric("💵 USD Equivalent", f"${wallet_usd_balance:,.2f}")

# --- SEND BITCOIN INTERFACE ---
st.subheader("📤 Send Bitcoin")

with st.form("send_btc_form"):
    recipient = st.text_input("Recipient BTC Address")
    amount_to_send = st.number_input("Amount to Send (BTC)", min_value=0.0001, max_value=wallet_btc_balance)
    token = st.text_input("🔐 Enter 6-digit Token Code", max_chars=6)
    submitted = st.form_submit_button("Send")

    if submitted:
        if not recipient or not token:
            st.error("❌ Please fill in all fields.")
        elif len(token) != 6 or not token.isdigit():
            st.error("❌ Invalid token code.")
        elif amount_to_send > wallet_btc_balance:
            st.error("❌ Amount exceeds wallet balance.")
        else:
            st.success(f"✅ {amount_to_send} BTC sent to `{recipient}` (Token verified).")

# --- TRANSACTION HISTORY ---
st.subheader("📄 Recent Transactions")
transactions = generate_transactions()

for tx in transactions:
    st.markdown(f"""
    **{tx['type']}** | `{tx['date']}`  
    Amount: `{tx['amount']} BTC`  
    Status: **{tx['status']}**  
    Tx Hash: `{tx['tx_hash']}`  
    {'📝 Description: ' + tx['description'] if tx.get('description') else ''}
    ---
    """)
