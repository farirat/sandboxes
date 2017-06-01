import argparse
from bittrex.bittrex import Bittrex
from api import my_orders, markets

parser = argparse.ArgumentParser(description='Bittrex api client.')
parser.add_argument('--myorders', nargs='*', default=None,
                    help='List my orders')
parser.add_argument('--sell-on-min-margin', default=None, type=int,
                    help='Sell if we have at least min margin')
parser.add_argument('--markets', nargs='*', default=None,
                    help='List my orders')

args = parser.parse_args()
MYORDERS = args.myorders is not None or args.sell_on_min_margin is not None
MARKETS = args.markets is not None

api = Bittrex('..', '..')

if MYORDERS:
    btc_balance, estimated_balance, total_orders, myorders = my_orders(api)
    print '############################'
    print 'Available BTC: %s' % btc_balance
    print 'Estimated balance / invested balance: ~%s / %s' % (estimated_balance, total_orders)

    print '############################'
    print 'My balances'
    print 'Coin         Cost (BTC)          Margin now    Balance       Ask price     Actual price '
    for myorder in myorders:
        print '%s%s%s%s%s%s' % (
            '{:<13}'.format(myorder['currency']),
            '{:<20}'.format(myorder['cost']),
            '{:<14}'.format(myorder['margin_now']),
            '{:<14}'.format(myorder['quantity']),
            '{:<14}'.format(myorder['price_on_buy']),
            '{:<13}'.format(myorder['actual_price']))

    if args.sell_on_min_margin:
        for myorder in myorders:
            if float(myorder['margin_now']) >= args.sell_on_min_margin:
                print 'Selling %s %s @ %s BTC:' % (myorder['quantity'], myorder['currency'], myorder['actual_price'])
                print api.sell_limit('BTC-%s' % myorder['currency'], myorder['quantity'], myorder['actual_price'])

if MARKETS:
    markets = markets(api)
    print '############################'
    print 'Coin summaries'
    print 'Coin         Note        24h Volume      Open buys Open sells 24h price variation '
    for k, v in markets.items():
        _note = ''
        if v['open_buys'] > v['open_sells']:
            _note += '!buys'
        if v['price_variation'] > 0.001:
            _note += '!pv'

        print '%s%s%s%s%s%s' % (
            '{:<13}'.format(k),
            '{:<12}'.format(_note),
            '{:<16}'.format(v['volume']),
            '{:<10}'.format(v['open_buys']),
            '{:<11}'.format(v['open_sells']),
            '{:<20}'.format(v['price_variation'])
        )
