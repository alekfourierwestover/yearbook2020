cd static 
npm i
cd ..
mkdir data
cd data

mkdir belmonthigh
cd belmonthigh
echo "{}" > users.json
echo "{}" > messages.json
echo "{}" > verification_codes.json
echo "{}" > passwords.json
echo "{}" > request.json

echo "[\"belmonthigh\"] " > registered_schools.json
echo "{ \"belmonthigh\": { \"senior\": [\"20@belmontschools.net\"], \"all\": [\"@belmontschools.net\", \"@belmont.k12.ma.us\"] } }" > school_email_patterns.json

