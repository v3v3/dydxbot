import math
import time
from pprint import pprint
from func_utils import format_number

# Place market order
def place_market_order(client, market, side, size, price, reduce_only):
    account = client.private.get_account()

    position_id = account.data["account"]["positionId"]

    # Get expiration time
    server_time = client.public.get_time()
    server_epoch_seconds = math.ceil(server_time.data["epoch"])
    expiration = server_epoch_seconds + 70

    # Place an order
    placed_order = client.private.create_order(
        position_id=position_id, # required for creating the order signature
        market=market,
        side=side,
        order_type="MARKET",
        post_only=False,
        size=size,
        price=price,
        limit_fee='0.015',
        expiration_epoch_seconds=expiration,
        time_in_force="FOK",
        reduce_only=reduce_only
    )

    return placed_order.data


# Abort all open positions
def abort_all_positions(client):
    
    # Cancel all orders
    client.private.cancel_all_orders()

    # Protect API
    time.sleep(0.5)

    # Get markets for reference of tick size
    markets = client.public.get_markets().data

    # Protect API
    time.sleep(0.5)

    # Get all open positions
    positions = client.private.get_positions(status="OPEN")
    all_positions = positions.data["positions"]

    # Handle open positions
    closed_orders = []
    if len(all_positions) > 0:
        
        # Loop through all positions
        for position in all_positions:
            
            # Determine the market
            market = position["market"]

            # Determine side
            side = "BUY"
            if position["side"] == "LONG":
                side = "SELL"
            
            # Get price
            price = float(position["entryPrice"])
            accept_price = price * 1.7 if side == "BUY" else price * 0.3
            tick_size = markets["markets"][market]["tickSize"]
            accept_price = format_number(accept_price, tick_size)

            # Place order to close
            order = place_market_order(
                client=client,
                market=market,
                side=side,
                size=position["sumOpen"],
                price=accept_price,
                reduce_only=True
            )

            # Append the result
            closed_orders.append(order)

            # Protect API
            time.sleep(0.2)
        
    # return closed orders
    return closed_orders