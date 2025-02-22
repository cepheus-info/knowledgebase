import numpy as np
import matplotlib.pyplot as plt
import argparse

def calculate_straddle_pnl(stock_prices, strike_price, premium_call, premium_put):
    pnl_call = np.maximum(stock_prices - strike_price, 0) - premium_call
    pnl_put = np.maximum(strike_price - stock_prices, 0) - premium_put
    return pnl_call + pnl_put

def calculate_strangle_pnl(stock_prices, strike_price_call, strike_price_put, premium_call, premium_put):
    pnl_call = np.maximum(stock_prices - strike_price_call, 0) - premium_call
    pnl_put = np.maximum(strike_price_put - stock_prices, 0) - premium_put
    return pnl_call + pnl_put

def calculate_vertical_spread_pnl(stock_prices, strike_price_long, strike_price_short, premium_long, premium_short, option_type):
    if option_type == 'call':
        pnl_long = np.maximum(stock_prices - strike_price_long, 0) - premium_long
        pnl_short = premium_short - np.maximum(stock_prices - strike_price_short, 0)
    else:
        pnl_long = np.maximum(strike_price_long - stock_prices, 0) - premium_long
        pnl_short = premium_short - np.maximum(strike_price_short - stock_prices, 0)
    
    # Calculate net debit/credit
    net_debit_credit = premium_long - premium_short
    
    # Total P&L
    total_pnl = pnl_long + pnl_short - net_debit_credit
    return total_pnl

def calculate_calendar_spread_pnl(stock_prices, strike_price, premium_near, premium_far):
    pnl_near = np.maximum(stock_prices - strike_price, 0) - premium_near
    pnl_far = np.maximum(stock_prices - strike_price, 0) - premium_far
    return pnl_far - pnl_near

def calculate_butterfly_spread_pnl(stock_prices, strike_price_low, strike_price_mid, strike_price_high, premium_low, premium_mid, premium_high):
    pnl_low = np.maximum(stock_prices - strike_price_low, 0) - premium_low
    pnl_mid = np.maximum(stock_prices - strike_price_mid, 0) - premium_mid
    pnl_high = np.maximum(stock_prices - strike_price_high, 0) - premium_high
    return pnl_low - 2 * pnl_mid + pnl_high

def calculate_condor_pnl(stock_prices, strike_price_low, strike_price_mid_low, strike_price_mid_high, strike_price_high, premium_low, premium_mid_low, premium_mid_high, premium_high):
    pnl_low = np.maximum(stock_prices - strike_price_low, 0) - premium_low
    pnl_mid_low = np.maximum(stock_prices - strike_price_mid_low, 0) - premium_mid_low
    pnl_mid_high = np.maximum(stock_prices - strike_price_mid_high, 0) - premium_mid_high
    pnl_high = np.maximum(stock_prices - strike_price_high, 0) - premium_high
    return pnl_low - pnl_mid_low - pnl_mid_high + pnl_high

def calculate_iron_condor_pnl(stock_prices, strike_price_call_short, strike_price_call_long, strike_price_put_short, strike_price_put_long, premium_call_short, premium_call_long, premium_put_short, premium_put_long):
    pnl_call_short = np.maximum(stock_prices - strike_price_call_short, 0) - premium_call_short
    pnl_call_long = np.maximum(stock_prices - strike_price_call_long, 0) - premium_call_long
    pnl_put_short = np.maximum(strike_price_put_short - stock_prices, 0) - premium_put_short
    pnl_put_long = np.maximum(strike_price_put_long - stock_prices, 0) - premium_put_long
    return pnl_call_short - pnl_call_long + pnl_put_short - pnl_put_long

def calculate_iron_butterfly_pnl(stock_prices, strike_price_call_short, strike_price_call_long, strike_price_put_short, strike_price_put_long, premium_call_short, premium_call_long, premium_put_short, premium_put_long):
    pnl_call_short = np.maximum(stock_prices - strike_price_call_short, 0) - premium_call_short
    pnl_call_long = np.maximum(stock_prices - strike_price_call_long, 0) - premium_call_long
    pnl_put_short = np.maximum(strike_price_put_short - stock_prices, 0) - premium_put_short
    pnl_put_long = np.maximum(strike_price_put_long - stock_prices, 0) - premium_put_long
    return pnl_call_short - pnl_call_long + pnl_put_short - pnl_put_long

def plot_pnl(stock_prices, pnl, title):
    plt.figure(figsize=(10, 6))
    plt.plot(stock_prices, pnl, label=title, color='blue')
    plt.axhline(0, color='black', linestyle='--')
    plt.axvline(stock_prices[len(stock_prices)//2], color='black', linestyle='--')
    plt.title(f'{title} Strategy P&L')
    plt.xlabel('Stock Price')
    plt.ylabel('Profit and Loss')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Options Strategy P&L Chart Generator')
    parser.add_argument('strategy', choices=['straddle', 'strangle', 'vertical_spread', 'calendar_spread', 'butterfly_spread', 'condor', 'iron_condor', 'iron_butterfly'], help='Options strategy type')
    parser.add_argument('--strike_price', type=float, help='Strike price for the options')
    parser.add_argument('--premium_call', type=float, help='Premium paid for the call option')
    parser.add_argument('--premium_put', type=float, help='Premium paid for the put option')
    parser.add_argument('--strike_price_call', type=float, help='Strike price for the call option (for strangle)')
    parser.add_argument('--strike_price_put', type=float, help='Strike price for the put option (for strangle)')
    parser.add_argument('--strike_price_long', type=float, help='Strike price for the long option (for vertical spread)')
    parser.add_argument('--strike_price_short', type=float, help='Strike price for the short option (for vertical spread)')
    parser.add_argument('--premium_long', type=float, help='Premium paid for the long option (for vertical spread)')
    parser.add_argument('--premium_short', type=float, help='Premium received for the short option (for vertical spread)')
    parser.add_argument('--strike_price_near', type=float, help='Strike price for the near-term option (for calendar spread)')
    parser.add_argument('--strike_price_far', type=float, help='Strike price for the far-term option (for calendar spread)')
    parser.add_argument('--premium_near', type=float, help='Premium paid for the near-term option (for calendar spread)')
    parser.add_argument('--premium_far', type=float, help='Premium paid for the far-term option (for calendar spread)')
    parser.add_argument('--strike_price_low', type=float, help='Lower strike price (for butterfly spread and condor)')
    parser.add_argument('--strike_price_mid', type=float, help='Middle strike price (for butterfly spread)')
    parser.add_argument('--strike_price_high', type=float, help='Higher strike price (for butterfly spread and condor)')
    parser.add_argument('--strike_price_mid_low', type=float, help='Lower middle strike price (for condor)')
    parser.add_argument('--strike_price_mid_high', type=float, help='Higher middle strike price (for condor)')
    parser.add_argument('--premium_low', type=float, help='Premium paid for the lower strike option (for butterfly spread and condor)')
    parser.add_argument('--premium_mid', type=float, help='Premium paid for the middle strike option (for butterfly spread)')
    parser.add_argument('--premium_high', type=float, help='Premium paid for the higher strike option (for butterfly spread and condor)')
    parser.add_argument('--premium_mid_low', type=float, help='Premium paid for the lower middle strike option (for condor)')
    parser.add_argument('--premium_mid_high', type=float, help='Premium paid for the higher middle strike option (for condor)')
    parser.add_argument('--strike_price_call_short', type=float, help='Strike price for the short call option (for iron condor and iron butterfly)')
    parser.add_argument('--strike_price_call_long', type=float, help='Strike price for the long call option (for iron condor and iron butterfly)')
    parser.add_argument('--strike_price_put_short', type=float, help='Strike price for the short put option (for iron condor and iron butterfly)')
    parser.add_argument('--strike_price_put_long', type=float, help='Strike price for the long put option (for iron condor and iron butterfly)')
    parser.add_argument('--premium_call_short', type=float, help='Premium received for the short call option (for iron condor and iron butterfly)')
    parser.add_argument('--premium_call_long', type=float, help='Premium paid for the long call option (for iron condor and iron butterfly)')
    parser.add_argument('--premium_put_short', type=float, help='Premium received for the short put option (for iron condor and iron butterfly)')
    parser.add_argument('--premium_put_long', type=float, help='Premium paid for the long put option (for iron condor and iron butterfly)')
    parser.add_argument('--stock_price_min', type=float, default=3000, help='Minimum stock price for the range')
    parser.add_argument('--stock_price_max', type=float, default=3500, help='Maximum stock price for the range')
    parser.add_argument('--stock_price_step', type=float, default=10, help='Step size for the stock price range')

    args = parser.parse_args()

    stock_prices = np.arange(args.stock_price_min, args.stock_price_max, args.stock_price_step)

    if args.strategy == 'straddle':
        if args.strike_price is None or args.premium_call is None or args.premium_put is None:
            parser.error('Straddle strategy requires --strike_price, --premium_call, and --premium_put')
        pnl = calculate_straddle_pnl(stock_prices, args.strike_price, args.premium_call, args.premium_put)
        plot_pnl(stock_prices, pnl, 'Straddle')
    elif args.strategy == 'strangle':
        if args.strike_price_call is None or args.strike_price_put is None or args.premium_call is None or args.premium_put is None:
            parser.error('Strangle strategy requires --strike_price_call, --strike_price_put, --premium_call, and --premium_put')
        pnl = calculate_strangle_pnl(stock_prices, args.strike_price_call, args.strike_price_put, args.premium_call, args.premium_put)
        plot_pnl(stock_prices, pnl, 'Strangle')
    elif args.strategy == 'vertical_spread':
        if args.strike_price_long is None or args.strike_price_short is None or args.premium_long is None or args.premium_short is None:
            parser.error('Vertical spread strategy requires --strike_price_long, --strike_price_short, --premium_long, and --premium_short')
        option_type = 'call' if args.premium_call is not None else 'put'
        pnl = calculate_vertical_spread_pnl(stock_prices, args.strike_price_long, args.strike_price_short, args.premium_long, args.premium_short, option_type)
        plot_pnl(stock_prices, pnl, 'Vertical Spread')
    elif args.strategy == 'calendar_spread':
        if args.strike_price is None or args.premium_near is None or args.premium_far is None:
            parser.error('Calendar spread strategy requires --strike_price, --premium_near, and --premium_far')
        pnl = calculate_calendar_spread_pnl(stock_prices, args.strike_price, args.premium_near, args.premium_far)
        plot_pnl(stock_prices, pnl, 'Calendar Spread')
    elif args.strategy == 'butterfly_spread':
        if args.strike_price_low is None or args.strike_price_mid is None or args.strike_price_high is None or args.premium_low is None or args.premium_mid is None or args.premium_high is None:
            parser.error('Butterfly spread strategy requires --strike_price_low, --strike_price_mid, --strike_price_high, --premium_low, --premium_mid, and --premium_high')
        pnl = calculate_butterfly_spread_pnl(stock_prices, args.strike_price_low, args.strike_price_mid, args.strike_price_high, args.premium_low, args.premium_mid, args.premium_high)
        plot_pnl(stock_prices, pnl, 'Butterfly Spread')
    elif args.strategy == 'condor':
        if args.strike_price_low is None or args.strike_price_mid_low is None or args.strike_price_mid_high is None or args.strike_price_high is None or args.premium_low is None or args.premium_mid_low is None or args.premium_mid_high is None or args.premium_high is None:
            parser.error('Condor strategy requires --strike_price_low, --strike_price_mid_low, --strike_price_mid_high, --strike_price_high, --premium_low, --premium_mid_low, --premium_mid_high, and --premium_high')
        pnl = calculate_condor_pnl(stock_prices, args.strike_price_low, args.strike_price_mid_low, args.strike_price_mid_high, args.strike_price_high, args.premium_low, args.premium_mid_low, args.premium_mid_high, args.premium_high)
        plot_pnl(stock_prices, pnl, 'Condor')
    elif args.strategy == 'iron_condor':
        if args.strike_price_call_short is None or args.strike_price_call_long is None or args.strike_price_put_short is None or args.strike_price_put_long is None or args.premium_call_short is None or args.premium_call_long is None or args.premium_put_short is None or args.premium_put_long is None:
            parser.error('Iron condor strategy requires --strike_price_call_short, --strike_price_call_long, --strike_price_put_short, --strike_price_put_long, --premium_call_short, --premium_call_long, --premium_put_short, and --premium_put_long')
        pnl = calculate_iron_condor_pnl(stock_prices, args.strike_price_call_short, args.strike_price_call_long, args.strike_price_put_short, args.strike_price_put_long, args.premium_call_short, args.premium_call_long, args.premium_put_short, args.premium_put_long)
        plot_pnl(stock_prices, pnl, 'Iron Condor')
    elif args.strategy == 'iron_butterfly':
        if args.strike_price_call_short is None or args.strike_price_call_long is None or args.strike_price_put_short is None or args.strike_price_put_long is None or args.premium_call_short is None or args.premium_call_long is None or args.premium_put_short is None or args.premium_put_long is None:
            parser.error('Iron butterfly strategy requires --strike_price_call_short, --strike_price_call_long, --strike_price_put_short, --strike_price_put_long, --premium_call_short, --premium_call_long, --premium_put_short, and --premium_put_long')
        pnl = calculate_iron_butterfly_pnl(stock_prices, args.strike_price_call_short, args.strike_price_call_long, args.strike_price_put_short, args.strike_price_put_long, args.premium_call_short, args.premium_call_long, args.premium_put_short, args.premium_put_long)
        plot_pnl(stock_prices, pnl, 'Iron Butterfly')

if __name__ == '__main__':
    main()