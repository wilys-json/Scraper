import argparse
import json

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
    parser = argparse.ArgumentParser()

    parser.add_argument("--alias", type=str, metavar="N",
                        help="Facebook alias")
    parser.add_argument("--email", type=str, metavar="EM",
                        help="Facebook login email")
    parser.add_argument("--password", type=str, metavar="PW",
                        help="Encoded facebook password")
    parser.add_argument("--no-auth", action="store_true", required=False,
                        help="Two-step authentication not required.")
    parser.add_argument("--jsonfile", type=str, default="setting.json",
                        metavar="F", help="config JSON filename")

    args = parser.parse_args()
    config = json.load(open(args.jsonfile))

    config['config']['TargetUrl'] = ("https://www.facebook.com/{}/photos"
                                    .format(args.alias))
    config['config']['usernameElement']['content'] = args.email
    config['config']['passwordElement']['content'] = args.password

    if args.no_auth:
        config['config']['loginSteps'] = LOGIN_STEPS['NoAuth']
    else:
        config['config']['loginSteps'] = LOGIN_STEPS['Auth']

    with open(args.jsonfile, 'w') as configFile:
        configJSON = json.dump(config, configFile, indent=4)


if __name__ == "__main__":
    main()
