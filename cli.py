import argparse
from bot import (
    BinanceFuturesClient,
    create_order_params,
    validate_order_inputs,
)
from bot.logging_config import setup_logging

logger = setup_logging("CLI")


def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")

    parser.add_argument("--symbol", required=True, help="Trading symbol (e.g. BTCUSDT)")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT", "STOP_LIMIT"])
    parser.add_argument("--quantity", type=float, required=True)
    parser.add_argument("--price", type=float)
    parser.add_argument("--stop-price", type=float)

    args = parser.parse_args()

    try:
        validate_order_inputs(args.type, args.price, args.stop_price)

        params = create_order_params(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
        )

        client = BinanceFuturesClient()
        order = client.create_order(**params)

        print("\nOrder placed successfully")
        print(f"Order ID: {order.get('orderId')}")
        print(f"Status: {order.get('status', 'UNKNOWN')}")
        print(f"Executed Qty: {order.get('executedQty')}")
        print(f"Avg Price: {order.get('avgPrice')}")

    except Exception as e:
        logger.error(e)
        print(f"\nOrder failed: {e}")


if __name__ == "__main__":
    main()
