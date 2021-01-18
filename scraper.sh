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


# Comment out the following line if you use Git Bash; change to `python` if error
# alias python3="winpty -Xallow-non-tty -Xplain python3"

# File alias
SCRIPT="script.json"
CONFIG="_config.py"
PROG="main.py"

cd Script

echo "Installing Python libraries..."
python3 -m pip3 install -q -r ../requirements.txt  # remove `python3 -m` if error

cls || clear

# Prompt for Facebook alias
echo -n "Please enter your Facebook alias:"
read ALIAS

# Prompt for Login email
echo -n "Please enter your Facebook login email:"
read EMAIL

# Prompt for Password
echo -n "Please enter your Facebook password:"
read -s Password
ENCODED=$(python3 $PROG --encode $Password -r)

# Ask if account login requires 2-step auth
echo "Does your Facebook account require Two-step Authentication?"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) python3 $CONFIG --alias $ALIAS --email $EMAIL\
              --password $ENCODED;
              break;;
        No ) python3 $CONFIG --alias $ALIAS --email $EMAIL\
             --password $ENCODED --no-auth;
             break;;

    esac
done

python3 $PROG --input $SCRIPT;  # Main program
python3 $CONFIG --revert;  # Revert config to template

cd ..

exit
