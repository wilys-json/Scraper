import argparse
import json
from Scraper import Scraper
from error import error
from time import sleep
from utils import _encode

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, metavar='I', required=False,
                        help='Input API.')
    parser.add_argument('--encode', type=str, metavar='ENC',required=False,
                        help='Encode string using Base64.')
    parser.add_argument('-r', '--reverse', action='store_true', required=False,
                        help='If flagged, encoded string will be reversed.')
    args = parser.parse_args()

    if args.encode:
        print(_encode(plain_text=args.encode, reverse=args.reverse))

    else:
        assert args.input, error.NOFILE("input")

        params = json.load(open(args.input))
        driver = Scraper(params['config'])

        for step in params['steps']:
            assert step in Scraper.__dict__, error.INVALID(step, "Step")
            Scraper.__dict__[step](driver)

        sleep(10)

if __name__ == '__main__':
    main()
