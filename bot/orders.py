def create_order_params(
    symbol,
    side,
    order_type,
    quantity,
    price=None,
    stop_price=None,
):
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"

    elif order_type == "STOP_LIMIT":
        params["price"] = price
        params["stopPrice"] = stop_price
        params["timeInForce"] = "GTC"

    return params
