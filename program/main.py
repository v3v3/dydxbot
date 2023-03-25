from func_connections import connect_dydx
from func_private import abort_all_positions
from func_public import construct_market_prices
from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED
from pprint import pprint

if __name__ == "__main__":
    print("hello bot")

    # Connect to client
    try:
        print("Connecting to client...")
        client = connect_dydx()
    except Exception as e:
        print(f"Error connecting to client: {e}")
        exit(1)

    # Abort all open positions
    if ABORT_ALL_POSITIONS:
        try:
            print("Closing all positions...")
            closed_orders = abort_all_positions(client=client)
        except Exception as e:
            print(f"Error closing all open positions: {e}")
            exit(1)

    # Find cointegrated pairs
    if FIND_COINTEGRATED:

        # Construct market prices
        try:
            print("Fetching market prices, please allow 3 mins...")
            df_market_prices = construct_market_prices(client=client)
        except Exception as e:
            print(f"Error constructing market prices: {e}")
            exit(1)
