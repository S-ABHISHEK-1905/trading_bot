def validate_order_inputs(order_type, price, stop_price, slices=None):
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("LIMIT orders require --price")

    if order_type == "STOP_LIMIT":
        if price is None or stop_price is None:
            raise ValueError("STOP_LIMIT orders require --price and --stop-price")

    if order_type == "TWAP":
        if slices is None or slices < 2:
            raise ValueError("TWAP orders require slices >= 2")
