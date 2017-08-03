sudo apt-get update;sudo apt-get upgrade -y
sudo apt-get install python-pip -y
sudo pip install -r requirements.txt
cd clickpirc
chmod +x runrcserver.py
cd ..
echo "Done"
echo "You can run, this two step."
echo "$ cd clickpirc/"
echo "$ sudo DJANGO_SETTINGS_MODULE=clickpirc.settings ./runrcserver.py"
