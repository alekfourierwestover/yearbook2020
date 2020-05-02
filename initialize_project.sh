cd static 
npm i
cd ..
echo "{}" > users.json
echo "{}" > messages.json

virtualenv venv
. venv/bin/activate

pip install requirements.txt
