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

import argparse
import json

# Scripts for Auth / No Auth Login
LOGIN_STEPS = {
    "Auth" : [
        "usernameElement",
        "passwordElement",
        "loginSubmitButton",
        "approvalCode",
        "checkpointSubmitButton",
        "saveBrowser",
        "checkpointSubmitButton"
    ],
    "NoAuth" : [
        "usernameElement",
        "passwordElement",
        "loginSubmitButton",
        "saveBrowser",
        "checkpointSubmitButton"
    ]
}


def main():
    """
    Helper program to configure scraping script.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--alias", type=str, metavar="N",
                        help="Facebook alias")
    parser.add_argument("--email", type=str, metavar="EM",
                        help="Facebook login email")
    parser.add_argument("--password", type=str, metavar="PW",
                        help="Encoded facebook password")
    parser.add_argument("--no-auth", action="store_true", required=False,
                        help="Two-step authentication not required.")
    parser.add_argument("--jsonfile", type=str, default="script.json",
                        metavar="F", help="config JSON filename")

    args = parser.parse_args()
    # Load JSON file
    config = json.load(open(args.jsonfile))

    # Configure targetUrl & login detail
    config['config']['TargetUrl'] = ("https://www.facebook.com/{}/photos"
                                    .format(args.alias))
    config['config']['usernameElement']['content'] = args.email
    config['config']['passwordElement']['content'] = args.password

    # Configure login option: Auth / No Auth
    if args.no_auth:
        config['config']['loginSteps'] = LOGIN_STEPS['NoAuth']
    else:
        config['config']['loginSteps'] = LOGIN_STEPS['Auth']

    # Write changes
    with open(args.jsonfile, 'w') as configFile:
        configJSON = json.dump(config, configFile, indent=4)


if __name__ == "__main__":
    main()
