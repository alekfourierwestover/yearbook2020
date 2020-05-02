cd static 
npm i
cd ..
echo "{}" > data/users.json
echo "{}" > data/messages.json

virtualenv venv
source venv/bin/activate

pip install -r requirements.txt

