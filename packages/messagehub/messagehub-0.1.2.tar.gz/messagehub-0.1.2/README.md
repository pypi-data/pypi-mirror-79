# messagehub [![Version][version-badge]][version-link] ![MIT License][license-badge]


messagehub: crypto and traditional financial data hub.
消息队列服务： 数字资产和传统资产数据队列服务，当前主要以数字资产为主，包含了传统的OHLCV数据，快讯数据，钱包数据，大额转账数据，DEFI数据，币种市场排名数据。    

include: 
bar data:  ohlcv for stock, crypto   
flash data: flash news of crypto symbols and stocks    
wallet data: blockchain labeling wallet 
transaction: blockchain  symbol large transactions 
defi data: uniswap pair transactions  
info data: coins market rank 

### Install

```
$ pip install messagehub
```

In China：    
```
$ pip install messagehub -i https://pypi.tuna.tsinghua.edu.cn/simple
```
 

### Usage

```
import messagehub as mh

token = "getapitokens"
api = mh.api(token)

# get crypto btc ohlcv in binance  获取现货kline数据 
code = "btcusdt"
exchange = "binance"
asset = "spot"
df = mh.bar(code, exchange=exchange, asset=asset)

# get 5m crypto perpetual ohlcv in binance with ma  获取永续合约kline数据
code = "btcusdt"
exchange = "binance"
asset = "perpetual"
freq = "5m"
ma = [7, 25, 99]
df = mh.bar(code, exchange=exchange, freq=freq, asset=asset, ma=ma)

# get 1d crypto perpetual ohlcv in binance with ma and time start end 
code = "btcusdt"
exchange = "binance"
asset = "perpetual"
freq = "1d"
ma = [7, 25, 99]
start = '20200201'
end = '20200802'
df = mh.bar(code, exchange=exchange, freq=freq, asset=asset, ma=ma, start_date=start, end_date=end)

# get flash data 快讯数据（jinse,bishijie,huoxing)
query = ""  
source_name = ""   # support jinse/bishijie/huoxing 
df = mh.flash(query, source_name)

# get wallet data  钱包数据
owner = "binance"
blockchain = "bitcoin"
symbol = "btc"
df = mh.wallet(owner, blockchain, symbol)

# get large transactions 大额转账数据
owner = ""      # binance , huobi ,
blockchain = "bitcoin"
symbol = "btc"
df = mh.transaction(owner, blockchain, symbol)

# get defi transactions 获取defi uniswap pair交易数据
contract_address = "0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852"
ret = mh.defi(contract_address, offset=1, limit=100)
print(ret.head(5))
ret.to_csv('defi_eth_usdt.csv', index=None)

# get info 获取支持的币种市场数据
df = mh.info()
df.to_csv('info.csv', index=None)

```


### License

[MIT](https://github.com/chaininout/messagehub/blob/master/LICENSE)


[version-badge]:   https://raw.githubusercontent.com/chaininout/messagehub/master/version-0.1-brightgreen.svg
[version-link]:    https://pypi.org/project/messagehub/
[license-badge]:   https://raw.githubusercontent.com/chaininout/messagehub/master/license.svg