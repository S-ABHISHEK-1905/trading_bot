import time
from bot.logging_config import setup_logging

logger = setup_logging("TWAP")


def execute_twap(
    client,
    symbol,
    side,
    total_quantity,
    slices,
    interval_seconds,
):
    slice_qty = round(total_quantity / slices, 8)
    orders = []

    logger.info(
        f"TWAP start | symbol={symbol} side={side} "
        f"total_qty={total_quantity} slices={slices} interval={interval_seconds}s"
    )

    for i in range(slices):
        logger.info(f"TWAP slice {i + 1}/{slices}")

        order = client.create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=slice_qty,
        )

        orders.append(order)

        if i < slices - 1:
            time.sleep(interval_seconds)

    logger.info("TWAP completed successfully")
    return orders
