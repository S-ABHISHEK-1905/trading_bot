import streamlit as st

from bot import (
    BinanceFuturesClient,
    create_order_params,
    validate_order_inputs,
    execute_twap,
)
from bot.logging_config import setup_logging

logger = setup_logging("StreamlitUI")

st.set_page_config(
    page_title="Binance Futures Trading Bot",
    page_icon="📈",
    layout="centered",
)

st.title("📈 Binance Futures Testnet Trading Bot")
st.caption("Menu-based Streamlit UI")

# ---------- Sidebar ----------
st.sidebar.header("Order Configuration")

symbol = st.sidebar.text_input("Symbol", value="BTCUSDT")
side = st.sidebar.selectbox("Side", ["BUY", "SELL"])
order_type = st.sidebar.selectbox(
    "Order Type",
    ["MARKET", "LIMIT", "STOP_LIMIT", "TWAP"],
)

quantity = st.sidebar.number_input(
    "Quantity",
    min_value=0.0,
    step=0.001,
    value=0.001,
)

price = None
stop_price = None
slices = None
interval = None

if order_type in ("LIMIT", "STOP_LIMIT"):
    price = st.sidebar.number_input("Price", min_value=0.0, step=0.1)

if order_type == "STOP_LIMIT":
    stop_price = st.sidebar.number_input("Stop Price", min_value=0.0, step=0.1)

if order_type == "TWAP":
    slices = st.sidebar.number_input("Slices", min_value=2, step=1, value=5)
    interval = st.sidebar.number_input("Interval (seconds)", min_value=1, step=1, value=10)

place_order = st.sidebar.button("🚀 Place Order")

# ---------- Preview ----------
st.subheader("Order Preview")

preview = {
    "Symbol": symbol,
    "Side": side,
    "Type": order_type,
    "Quantity": quantity,
}

if price:
    preview["Price"] = price
if stop_price:
    preview["Stop Price"] = stop_price
if order_type == "TWAP":
    preview["Slices"] = slices
    preview["Interval"] = interval

st.json(preview)

# ---------- Execution ----------
if place_order:
    try:
        client = BinanceFuturesClient()

        if order_type == "TWAP":
            validate_order_inputs(order_type, None, None, slices)

            with st.spinner("Executing TWAP strategy..."):
                orders = execute_twap(
                    client=client,
                    symbol=symbol,
                    side=side,
                    total_quantity=quantity,
                    slices=slices,
                    interval_seconds=interval,
                )

            st.success("✅ TWAP execution completed")
            st.write(f"Orders executed: {len(orders)}")

        else:
            validate_order_inputs(order_type, price, stop_price)

            params = create_order_params(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
                stop_price=stop_price,
            )

            with st.spinner("Placing order..."):
                order = client.create_order(**params)

            st.success("✅ Order placed successfully")
            st.write(f"Order ID: {order.get('orderId')}")
            st.write(f"Status: {order.get('status')}")
            st.write(f"Executed Qty: {order.get('executedQty')}")
            st.write(f"Avg Price: {order.get('avgPrice')}")

    except Exception as e:
        logger.error(e)
        st.error(f"❌ Order failed: {e}")
