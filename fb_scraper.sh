echo "Installing Python libraries..."
pip3 install -q -r requirements.txt

cls || clear

echo -n "Please enter your Facebook alias:"
read ALIAS

echo -n "Please enter your Facebook login email:"
read EMAIL

echo -n "Please enter your Facebook password:"
read -s Password
ENCODED=$(python3 fb_scraper.py --encode $Password -r)

echo "Does your Facebook account require Two-step Authentication?"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) python3 _config.py --alias $ALIAS --email $EMAIL\
              --password $ENCODED;
              python3 fb_scraper.py --input setting.json;
              exit;;
        No ) python3 _config.py --alias $ALIAS --email $EMAIL\
             --password $ENCODED --no-auth;
             python3 fb_scraper.py --input setting.json;
             exit;;
    esac
done
