# Facebook Photo Scraper

A scraper to retrieve "Photos of You" on Facebook

## Requirements
[Python 3.7+](https://www.python.org/downloads/release/python-379/) - built-in on MacOS 10.15

[Git Bash](https://git-scm.com/download/win) - *for Windows 10*


## Usage
Download:
```
$ git clone https://github.com/wlamcuhk/Scraper.git
$ cd Scraper
```

If you are using *Windows 10* and have downloaded Git, open `scraper.sh` and uncomment the following line:
```
alias python3="winpty -Xallow-non-tty -Xplain python3"
```

To run the program:
```
$ bash scraper.sh
```
or open the file with Git Bash on *Windows 10*

Input login information:
```
Please enter your Facebook alias: $YOUR_FACEBOOK_ALIAS
Please enter your Facebook login email: $YOUR_LOGIN_EMAIL
Please enter your Facebook password: $YOUR_PASSWORD
Does your Facebook account require Two-step Authentication?
1) Yes
2) No
#?
$ (Type `1` and hit Enter if Yes, otherwise `2`)
```

*For 2-step Authentication, please get your Authentication code ready:*
```
Please enter approvals_code: $AUTHENTICATION_CODE
```

*Note: Please verify your login via email or push notification on your phone, or Facebook will temporarily lock your account!*

And Voila! When the program finishes running, you should find all your `Photos of You` under a directory called `PhotosOfMe`.


## Troubleshooting

***Traceback***

If the program breaks while scraping and shows the following Traceback:
```
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//img[contains(@src, "jpg")]"}
  (Session info: chrome=87.0.4280.141)
```
This is because the photo element is not yet loaded when the program tries to retrieve it.

To avoid this, you can modify the `Wait` and `LongWait` time in the `Script/script.json` file:

```
{
    "config": {
        ...
        "Wait": $CHANGE THIS TO A LARGER VALUE,
        "LongWait": $CHANGE THIS TO A LARGER VALUE,
        ...
```

***Command-line Errors***

*Windows Git Bash*

Make sure you have commented out [the line as stated](#usage)

If the command `python3` is not recognized, try change `python3` to `python`, i.e.
```
alias python3="winpty -Xallow-non-tty -Xplain python"
```

*pip3 Command*

If the line `python3 -m pip3 install -q -r ../requirements.txt` is not run properly, change this to:
```
pip3 install -q -r ../requirements.txt
```

## Customization

The default path of the download folder is `../PhotosOfMe`, you can change this name by altering the following in `Script/script.json`:
```
{
    "config": {
        ...
        "downloadDirectory": "$CHANGE THIS TO YOUR TARGET DIRECTORY",
        ...

```
<span style = "font-size: 9pt">*Note: `script.json` is under the folder `Script`, make sure you navigate up the directory if you want to save outside the `Script` folder*</span>

## License

Copyright(c) 2021 Wilson Lam, The [MIT](./LICENSE) License
