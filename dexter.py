import argparse
import json
import time

import requests


from logger import get_logger



logger = get_logger(__name__)


url = "https://api.dexscreener.com/token-profiles/latest/v1"
rug_check_url = "https://api.rugcheck.xyz/v1/tokens/"


def get_dex_data(url=url):
    try:
        response = requests.get(url)
        data = response.json()
        data = [
            {
                "token_address" : x.get("tokenAddress")
            } for x in data if x.get("chainId") == "solana"
        ]
    except Exception as error:
        return False, None
    return True, data



def analyze_token(token, url=rug_check_url):
    try:

        token_url = f"{url}{token}/report"
        response = requests.get(token_url)
        response.raise_for_status()
        data = response.json()
        
        stats = {
            "name": data.get("tokenMeta", {}).get("name", "N/A"),
            "symbol": data.get("tokenMeta", {}).get("symbol", "N/A"),
            "supply": data.get("token", {}).get("supply", 0),
            "decimals": data.get("token", {}).get("decimals", 0),
            "total_market_liquidity": data.get("totalMarketLiquidity", 0),
            "top_holders_distribution": [
                {
                    "address": holder.get("address"),
                    "amount": holder.get("uiAmount"),
                    "percentage": holder.get("pct")
                }
                for holder in data.get("topHolders", [])
            ],
            "score": data.get("score", 0),
            "risks": [
                {
                    "name": risk.get("name"),
                    "description": risk.get("description"),
                    "level": risk.get("level")
                }
                for risk in data.get("risks", [])
            ],
            "rugged": data.get("rugged", False),
            "total_lp_providers": data.get("totalLPProviders", 0),
            "lp_locked_pct": data.get("markets", [{}])[0].get("lpLockedPct", 0),
            "lp_locked_usd": data.get("markets", [{}])[0].get("lpLockedUSD", 0),
        }
        
        analysis = {
            "is_good_token": stats["score"] >= 500 and not stats["rugged"],
            "has_significant_liquidity": stats["total_market_liquidity"] > 50000,
            "holder_concentration": {
                "high_concentration": any(holder["percentage"] > 30 for holder in stats["top_holders_distribution"]),
                "low_concentration": all(holder["percentage"] < 5 for holder in stats["top_holders_distribution"]),
            },
        }
        
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching token data: {e}")
        return None

    return {"stats": stats, "analysis": analysis}



def main(args):
    logger.info("[CoiNs CoiNs] *discalimer* research coins before hand;")
    logger.info("[re$ults] ----------------------------------------------")
    
    status, data = get_dex_data()

    if not status:
        logger.info("[error] Unable to get dex data .. exiting")
        exit(0)

    for each in data:
        time.sleep(0.25)
        token_address = each.get("token_address")
        try:
            resp = requests.get(
                "https://api.dexscreener.com/latest/dex/tokens/%s" % each.get(
                    "token_address"
                )
            )
            if resp.status_code != 200:
                raise Exception(
                    "Could not get coin with token %s" % each.get("token_address")
                )
            data = resp.json()
        except Exception as error:
            continue

        min_liquidity_usd = args.min_liquidity
        min_marketcap_usd = args.min_marketcap_usd
        max_marketcap_usd = args.max_marketcap_usd
        max_age_hours = args.max_age_hours
        min_24h_buys = args.min_24h_buys
        min_24h_sells = args.min_24h_sells
        min_volume_24h = args.min_volume
        
        ############################
        # sum of buys and sells during the last 5 minutes.
        ####################

        min_5m_txns = args.min_5m_txns
        current_time_ms = int(time.time() * 1000)
        filtered_pairs = []

        for pair in data["pairs"]:
            try:
                liquidity_usd = pair["liquidity"]["usd"]
            except KeyError:
                liquidity_usd = 0
            marketcap = pair.get("marketCap", 0)
            pair_created_at = pair["pairCreatedAt"]
            age_ms = current_time_ms - pair_created_at
            age_hours = age_ms / (1000 * 60 * 60)
            buys_24h = pair["txns"]["h24"]["buys"]
            sells_24h = pair["txns"]["h24"]["sells"]
            buys_5m = pair["txns"]["m5"]["buys"]
            sells_5m = pair["txns"]["m5"]["sells"]
            volume_24h = pair["volume"]["h24"]
            total_5m_txns = buys_5m + sells_5m

            if (liquidity_usd >= min_liquidity_usd and
                min_marketcap_usd <= marketcap <= max_marketcap_usd and
                age_hours <= max_age_hours and
                buys_24h >= min_24h_buys and
                sells_24h >= min_24h_sells and
                total_5m_txns >= min_5m_txns and
                volume_24h >= min_volume_24h):
                filtered_pairs.append(pair)


        if filtered_pairs:
            for p in filtered_pairs:
                logger.info("")
                logger.info("[CoiN] *discalimer* research coin before hand; $v$")
                name = p["baseToken"]["name"]
                symbol = p["baseToken"]["symbol"]
                market_cap = p["marketCap"]
                try:
                    liquidity = p["liquidity"]["usd"]
                except KeyError:
                    liquidity = 0
                pair_url = p["url"]
                volume_24h = p["volume"]["h24"]
                buys_24 = p["txns"]["h24"]["buys"]
                sells_24 = p["txns"]["h24"]["sells"]
                age = (current_time_ms - p["pairCreatedAt"]) / (1000.0 * 60.0 * 60.0)
                price = p.get("priceUsd", "no-price-set") 
                if price == "no-price-set":
                    price = 0.00
                else:
                    price = float(price)
                logger.info(f"Token Name: {name} ({symbol})")
                logger.info(f"Token address: {token_address}")
                logger.info(f"  Price: {price}")
                logger.info(f"  Market Cap: ${market_cap:,.2f}")
                logger.info(f"  Liquidity: ${liquidity:,.2f}")
                logger.info(f"  24h Volume: ${volume_24h:,.2f}")
                logger.info(f"  24h Transactions: Buys={buys_24}, Sells={sells_24}")
                logger.info(f"  Pair Age: {age:.2f} hours")
                logger.info(f"  More info: {pair_url}")
                
                if not args.run_risk_sentiment_analysis:
                    logger.info("-" * 40)
                    logger.info("")
                    continue

                result = analyze_token(token_address)
                logger.info("")
                if result:
                    logger.info("Token Trust Score:")
                    for key, value in result["stats"].items():
                        if key == "top_holders_distribution":
                            pass
                        elif key == "risks":
                            logger.info("")
                            logger.info("Token Risks")
                            for risk in value:
                                name = risk.get("name")
                                description = risk.get("description")
                                logger.info("  Name %s" % name)
                                logger.info("     Description %s" % description)
                        else:
                            logger.info(f"  {key}: {value}")
                    
                    # TOKEN ANALYSIS
                    logger.info("")
                    logger.info("Token Analysis:")
                    for key, value in result["analysis"].items():
                        if key == "holder_concentration":
                            logger.info("")
                            logger.info("Holder Concentration")
                            logger.info("  high_concentration: %s" % value["high_concentration"])
                            logger.info("  low_concentration: %s" % value["low_concentration"])
                            logger.info("")
                        else:
                            logger.info(f"  {key}: {value}")
                else:
                    logger.info("No Trust Score Found!")

                logger.info("-" * 40)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter tokens based on various criteria.")
    parser.add_argument('--min-liquidity', type=float, default=8500,
                        help='Minimum required liquidity in USD (default: 8500).')
    parser.add_argument('--min-marketcap-usd', type=float, default=200000,
                        help='Minimum market cap in USD (default: 200000).')
    parser.add_argument('--max-marketcap-usd', type=float, default=500000,
                        help='Maximum market cap in USD (default: 500000).')
    parser.add_argument('--max-age-hours', type=float, default=1,
                        help='Maximum pair age in hours (default: 1).')
    parser.add_argument('--min-24h-sells', type=int, default=50,
                        help='Minimum number of sells in the last 24 hours (default: 50).')
    parser.add_argument('--min-24h-buys', type=int, default=50,
                        help='Minimum number of buys in the last 24 hours (default: 50).')
    parser.add_argument('--min-volume', type=float, default=13000,
                        help='Minimum 24h volume in USD (default: 13000).')
    parser.add_argument('--min-5m-txns', type=int, default=10,
                        help='Minimum number of transactions in the last 5 minutes (default: 10).')
    parser.add_argument('--run-risk-sentiment-analysis', action='store_true', default=False,
                    help='Run token risk sentiment analysis with rugcheck (default yes).')
    args = parser.parse_args()

    main(args)
