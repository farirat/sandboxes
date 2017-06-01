import argparse
import sys
from bittrex.bittrex import Bittrex

parser = argparse.ArgumentParser(description='Bittrex buyer client.')
parser.add_argument('--market', type=str, required=True,
                    help='Market to buy (ex: BTC-LTC)')
parser.add_argument('--price', choices=['last', 'bid', 'ask'], required=True,
                    help='Price (last, bid or ask)')
parser.add_argument('--total-btc', type=float, required=True,
                    help='Total value in BTC')

args = parser.parse_args()

api = Bittrex('8e29aae2c3f34ee889644d46afbd0a38', '1c6013d5e81d47e6b0bd66fdaf4457d7')

ticker = api.get_ticker(args.market)['result']
quantity = args.total_btc / ticker[args.price.title()]
print 'Buying %s %s @ %s BTC:' % (quantity, args.market, args.total_btc)
print api.buy_limit(args.market, quantity, ticker[args.price.title()])
