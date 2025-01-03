import argparse
import json
import re
import sys

import requests

from logger import get_logger


logger = get_logger(__name__)


def main(args):

    market_cap_from = args.market_cap_from
    market_cap_to = args.market_cap_to
    volume_from = args.volume_from

    url = f"https://advanced-api.pump.fun/coins/"
    url += f"list?sortBy=creationTime&marketCapFrom={market_cap_from}"
    url += f"&marketCapTo={market_cap_to}&volumeFrom={volume_from}"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        logger.error(f"An error occurred while fetching data: {error}")
        exit(1)

    data = response.json()
    matches_list = []
    for coin in data:
        name = coin.get("name").lower()

        ####################################################
        # Check num holders
        ####################################################
        
        num_holders = coin.get("numHolders")
        if args.min_holders is not None:
            if num_holders >= args.min_holders:
                pass
            else:
                continue
        
        ###################################################
        # Check name match
        ###################################################

        if args.name_match is None:
            matches_list.append(coin)
        if args.name_match is not None and name.__contains__(args.name_match):
            matches_list.append(coin)


    logger.info("[ReSulTs] foUnd: %s" % len(matches_list))
    matches_list = sorted(
        matches_list, 
        key=lambda x: x["marketCap"], 
        reverse=True
    )
    for coin in matches_list:
        coin_id = coin.get("coinMint")
        dev = coin.get("dev")
        name = coin.get("name")
        ticker = coin.get("ticker")
        creation_time = coin.get("creationTime")
        number_of_holders = coin.get("numHolders")
        market_capital = coin.get("marketCap")
        volume = coin.get("volume")
        bonding_curve_progress = coin.get("bondingCurveProgress")
        sniper_count = coin.get("sniperCount")
        current_market_price = coin.get("currentMarketPrice")
        holders = coin.get("holders")
         
        logger.info("[CoIn Info]")
        logger.info(f"  Name: {name}")
        logger.info(f"  Ticker: {ticker}")
        logger.info(f"  CoinId: {coin_id}")
        logger.info(f"  Market Cap {market_capital}")
        logger.info(f"  Volume: {volume}")
        logger.info(f"  Total Holders: {number_of_holders}")
        logger.info(f"  Bonding Curve Progress: {bonding_curve_progress}")
        logger.info(f"  Sniper Count: {sniper_count}")
        logger.info(f"  Current Market Price: {current_market_price}")
        logger.info("-" * 40) 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Fetch coins by market cap range "
            "from advanced pump fun reversed frontend api."
        )
    )
    parser.add_argument(
        "--market-cap-from", 
        type=int, 
        default=0, 
        help="Minimum market cap"
    )
    parser.add_argument(
        "--market-cap-to", 
        type=int, 
        default=800000, 
        help="Maximum market cap (default: 190000)"
    )
    parser.add_argument(
        "--volume-from",
        type=float,
        default=0.00,
        help="volume from"
    )
    parser.add_argument(
        "--name-match",
        type=str,
        help="string to match a coins name"
    )
    parser.add_argument(
        "--min-holders",
        type=int,
        help="max holders of a coin"
    )
    args = parser.parse_args()

    main(args)

