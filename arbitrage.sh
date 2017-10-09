#!/bin/bash
declare -a markets=('_1broker' '_1btcxe' 'bit2c' 'bitcoincoid' 'bitfinex' 'bitmex' 'bitso' 'bittrex' 'btcchina' 'bxinth' 'coinsecure' 'fybse' 'fybsg' 'gdax' 'hitbtc' 'huobi' 'jubi' 'kraken', 'okcoincny' 'poloniex' 'quadrigacx' 'therock' 'vaultoro' 'virwox' 'yobit')
for i in "${markets[@]}"
 do
    :
    bash -c "python get_price_info.py $i BTC/USD save_price > /dev/null"  &
 done

while true
   do sleep 1000
 done
