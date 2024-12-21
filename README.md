### Coins Coins


The script only support solana coins -- uses dexscreener api, tweak options or code.


#### How to RUN:

> if you run with --risk-sentiment-analysis ensure that you are running the script with proxysocks or proxies, since it uses `rugcheck.xyz` and they have a rate limiter.

for dexscreen

```
usage: dexter.py [-h] [--min-liquidity MIN_LIQUIDITY] [--min-marketcap-usd MIN_MARKETCAP_USD] [--max-marketcap-usd MAX_MARKETCAP_USD] [--max-age-hours MAX_AGE_HOURS] [--min-24h-sells MIN_24H_SELLS] [--min-24h-buys MIN_24H_BUYS] [--min-volume MIN_VOLUME]
                 [--min-5m-txns MIN_5M_TXNS] [--run-risk-sentiment-analysis]

Filter tokens based on various criteria.

options:
  -h, --help            show this help message and exit
  --min-liquidity MIN_LIQUIDITY
                        Minimum required liquidity in USD (default: 8500).
  --min-marketcap-usd MIN_MARKETCAP_USD
                        Minimum market cap in USD (default: 200000).
  --max-marketcap-usd MAX_MARKETCAP_USD
                        Maximum market cap in USD (default: 500000).
  --max-age-hours MAX_AGE_HOURS
                        Maximum pair age in hours (default: 1).
  --min-24h-sells MIN_24H_SELLS
                        Minimum number of sells in the last 24 hours (default: 50).
  --min-24h-buys MIN_24H_BUYS
                        Minimum number of buys in the last 24 hours (default: 50).
  --min-volume MIN_VOLUME
                        Minimum 24h volume in USD (default: 13000).
  --min-5m-txns MIN_5M_TXNS
                        Minimum number of transactions in the last 5 minutes (default: 10).
  --run-risk-sentiment-analysis
                        Run token risk sentiment analysis with rugcheck (default yes).

```

for pumpfun

```
usage: pump_fun.py [-h] [--market-cap-from MARKET_CAP_FROM] [--market-cap-to MARKET_CAP_TO] [--volume-from VOLUME_FROM] [--name-match NAME_MATCH] [--check-if-holders-are-scammers CHECK_IF_HOLDERS_ARE_SCAMMERS]

Fetch coins by market cap range from advanced pump fun reversed frontend api.

options:
  -h, --help            show this help message and exit
  --market-cap-from MARKET_CAP_FROM
                        Minimum market cap
  --market-cap-to MARKET_CAP_TO
                        Maximum market cap (default: 190000)
  --volume-from VOLUME_FROM
                        volume from
  --name-match NAME_MATCH
                        string to match a coins name
```
