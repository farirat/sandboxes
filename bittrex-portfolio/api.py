
def my_orders(api):
    # 1. Get balances
    balances = api.get_balances()
    btc_balance = estimated_balance = total_orders = 0
    myorders = []
    for balance in balances['result']:
        if balance['Currency'] == 'BTC':
            btc_balance = balance['Available']
            continue
        if balance['Available'] == 0:
            continue

        #print 'Getting BTC-%s (%s %s)' % (balance['Currency'], balance['Available'], balance['Currency'])
        history = api.get_order_history('BTC-%s' % balance['Currency'], 10)
        ticker = api.get_ticker('BTC-%s' % balance['Currency'])
        _order_balance = 0

        for order in history['result']:
            if _order_balance >= balance['Available']:
                break

            _order_balance += order['Quantity']

            myorders.append({
                'currency': balance['Currency'],
                'cost': order['PricePerUnit'] * order['Quantity'],
                'quantity': order['Quantity'],
                'closed': order['Closed'],
                'price': order['Price'],
                'price_on_buy': order['PricePerUnit'],
                'actual_price': ticker['result']['Last'],
                'margin_now': '%f' % ((ticker['result']['Last'] / order['PricePerUnit']) * 100),
            })

            estimated_balance += order['Quantity'] * ticker['result']['Last']
            total_orders += order['Quantity'] * order['PricePerUnit']

    return btc_balance, estimated_balance, total_orders, myorders


def markets(api):
    # 2. Get markets
    print 'Getting market summaries'
    markets = {}
    for market in api.get_market_summaries()['result']:
        markets[market['MarketName']] = {
            'volume': market['Volume'],
            'open_buys': market['OpenBuyOrders'],
            'open_sells': market['OpenSellOrders'],
            'price_variation': market['PrevDay'] - market['Last']
        }

    print market
    return markets