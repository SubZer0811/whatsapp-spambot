pip3 install splinter
pip3 install argparse
wget https://github.com/mozilla/geckodriver/releases/download/v0.27.0/geckodriver-v0.27.0-linux64.tar.gz
tar -xvf geckodriver-v0.27.0-linux64.tar.gz 
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/
sudo rm geckodriver*