###################################################################################
# The MIT License (MIT)                                                           #
#                                                                                 #
# Copyright (c) 2021 Wilson Lam                                                   #
#                                                                                 #
# Permission is hereby granted, free of charge, to any person obtaining a copy of #
# this software and associated documentation files (the "Software"), to deal in   #
# the Software without restriction, including without limitation the rights to    #
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of#
# the Software, and to permit persons to whom the Software is furnished to do so, #
# subject to the following conditions:                                            #
#                                                                                 #
# The above copyright notice and this permission notice shall be included in all  #
# copies or substantial portions of the Software.                                 #
#                                                                                 #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS#
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR  #
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER  #
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN         #
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.      #
###################################################################################

import sys
sys.path.append('../')

import os
import argparse
import json
from Scraper.scraper import Scraper
from Scraper.error import error
from time import sleep
from Scraper.utils import _encode

def main():
    """
    Main program of Scraper.
    `--input` option calls the scraping program.
    `--encode` option calls the encode password program.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, metavar='I', required=False,
                        help='Input API.')
    parser.add_argument('--encode', type=str, metavar='ENC',required=False,
                        help='Encode string using Base64.')
    parser.add_argument('-r', '--reverse', action='store_true', required=False,
                        help='If flagged, encoded string will be reversed.')
    args = parser.parse_args()

    # Encode password
    if args.encode:
        print(_encode(plain_text=args.encode, reverse=args.reverse))

    # Call scraping script
    else:
        assert os.path.exists(args.input), error.NOFILE("input", args.input)

        # Load JSON file
        params = json.load(open(args.input))
        # Configure Scraper object
        driver = Scraper(params['config'])

        # Imeplement steps in scraping script
        for step in params['steps']:
            assert step in Scraper.__dict__, error.INVALID(step, "Step")
            Scraper.__dict__[step](driver)

if __name__ == '__main__':
    main()
