
# coding: utf-8

# Import Files

# In[1]:

import time
from database import create_db, create_table, insert_data
from datetime import datetime
import sys


market_list = ['_1broker', '_1btcxe', 'bit2c', 'bitcoincoid', 'bitfinex', 'bitmex', 'bitso', 'bittrex',
               'btcchina', 'bxinth', 'coinsecure', 'fybse', 'fybsg', 'gdax', 'hitbtc', 'huobi', 'jubi', 'kraken',
               'okcoincny', 'poloniex', 'quadrigacx', 'therock', 'vaultoro', 'virwox', 'yobit']


# Import market class

# In[3]:

def _import_market_class(class_name):
    return getattr(__import__('ccxt'), class_name)


# Classify market by symbol

# In[4]:

def _classify_market_symbol():
    market_instances_dict = dict()
    print('In Progress...')

    for market in market_list:
        market_instance = _import_market_class(market)()

        try:
            market_instance.load_products()
        except:
            print('Load products error: ', market_instance.id)
            continue

        market_symbols = market_instance.symbols

        for each_symbol in market_symbols:
            if each_symbol in market_instances_dict:
                market_instances_dict[each_symbol] += [market_instance]
            else:
                market_instances_dict[each_symbol] = [market_instance]

    return market_instances_dict


# Pair market by symbol

# In[5]:

def _match_market_pair():
    market_pair_list = list()
    market_instances_dict = _classify_market_symbol()

    for each_symbol in market_instances_dict:
        each_market_instances_list = market_instances_dict[each_symbol]
        main_index = 0
        while main_index < len(each_market_instances_list) - 1:
            index = main_index + 1
            while index < len(each_market_instances_list):
                    market_pair_list.append({'pair':'{0}_{1}'.format(each_market_instances_list[main_index].id,
                                                                     each_market_instances_list[index].id),
                                                         'symbol': each_symbol,
                                                         'country_pair':'{0}:{1}'.format(each_market_instances_list[main_index].countries,
                                                                                         each_market_instances_list[index].countries)})
                    index += 1
            main_index += 1

    return market_pair_list


# Display market pair in specified symbol

# In[6]:

def available_pair_market(symbol='all'):
    pair_list = _match_market_pair()
    print('Region', '{}'.format(' ' * 17), 'Pair', '{}'.format(' ' * 10), 'Symbol' )

    number = 1
    for each_pair in pair_list:
        if each_pair['symbol'] == symbol or symbol == 'all':
            str_number = str(number) + '.'
            print(str_number, each_pair['country_pair'], '{}'.format(' ' * (10 - len(str_number))),
                  each_pair['pair'], '{}'.format(' ' * (21 - len(each_pair['pair']))), each_pair['symbol'])
            number += 1


# In[7]:

# Save price data to database

# In[ ]:

class MarketData:
    def __init__(self, market='bitmex', symbol='BTC/USD'):
        assert (market in market_list), 'Market is not in market list'
        self.market = market
        self.market_instance = self._instantiate_market()
        self._load_products(self.market_instance)

        assert (symbol in self.market_instance.symbols), symbol + ' is not'
        self.symbol = symbol

    def _instantiate_market(self):
        return _import_market_class(self.market)()

    def _load_products(self, market_instance):
        return self.market_instance.load_markets()

    def _get_tickers(self, market_instance):
        try:
            return market_instance.fetch_ticker(self.symbol)

        except:
            return False

    def _get_orderbook(self, market_instance):
        try:
            return market_instance.fetchOrderBook(self.symbol)

        except:
            return False

    def save_price(self):
        create_db()
        create_table()

        while True:
            start = time.time()

            orderbook = self._get_orderbook(self.market_instance)
            end_tick = time.time()

            if orderbook != False:
                is_insert = insert_data(orderbook, self.market, self.symbol,  end_tick - start)
                if is_insert:
                    end = time.time()
                    print('Get tick at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'CPU Time:', end - start)

            else:
                end = time.time()
                print('Fail to get tick at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'CPU Time:', end - start )


# In[ ]:1
assert len(sys.argv) > 1, 'Invalid number of argument'
attributes = sys.argv[1:-1]
behavior = sys.argv[-1]

if len(sys.argv) == 2 or len(sys.argv) == 3:
    globals()[behavior](*attributes)

else:
    while True:
        market = MarketData(*attributes)
        method = getattr(market, sys.argv[-1])
        method()

#available_pair_market('BTC/USD')
#bitmex = MarketData('bitmex', 'BTC/USD')
#bitmex.save_price()


# In[ ]:
