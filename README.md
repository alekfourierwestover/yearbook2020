# yearbook2020
Yearbook for BHS 2020

# project installation

```
git clone https://github.com/alekfourierwestover/yearbook2020.git
cd static
npm i
cd ..

mkdir data
cd data

mkdir belmonthigh
cd belmonthigh

<<<<<<< HEAD
echo "{}" > data/users.json
echo "{}" > data/messages.json
=======
echo "{}" > users.json
echo "{}" > messages.json
>>>>>>> 0c1d526d08457edc6c7a939862c6bb7789881932
echo "{}" > passwords.json
echo "{}" > request.json
echo "{}" > verification_codes.json

cd ..

echo "["belmonthigh"]" > registered_schools.json

echo "{
  "belmonthigh": {
    "senior": ["20@belmontschools.net"],
    "all": ["@belmontschools.net", "@belmont.k12.ma.us"]
  }
}" > school_email_patterns.json

cd .. (get to the yearbook directory)

python3 app.py




virtualenv venv
source venv/bin/activate

pip install -r requirements.txt
```

then to run:

```
nohup python app.py &
```

#TODO 5/5/20
- cleo card  [all]
  - send messages feature that is public
  - link to go fund me
- make the request menu better [leon]
- teacher menu [leon]
- how to use page [david]
- encrypting messages [dr. westover md phd mba jd]
- make edit pfp not require hard reload for img to change [all]
- make check marks work and work beautifully [alek]
- confetti? [madeline]


# Bugs 4/27/20 

# unresolved
- password resets
- outside emails?  - keep the 20@belmontschools.net => if not, look through teacher email list   

- map
	- maurader head map stuff is squished
	- dumb blank space at the bottom

- misc:
	- static pages

# resolved
- edit profile: change quote / change password : wrong password --> logs you out - desired behavior: tells you try again
- need length restriction on qutoe and name
- login and register w/o entering anything returns internal server error
- verify has no style
- resend verification code throws internal server error
- sendmessages can submit empty message (not a real issue)
- need length restriction on qutoe and name
- main - Names should be alphabetical
- shouldn't be able to create an account over someone elses account
- server stuff: - should need to be logged in to get your messages
- verify - you shouldn't show up on main until you have a verified account


#TODO 4/22/20
- Ziyong: checkmarks next to names; responsive web design (main; text; pictures); increase text size; sendmessages css two columns
- Leon: notify.js; login page (make two columns) => css; lowercase names (not case-sensitive); login css
- Andrew: navbar (make it a drop down) (make separate file for navbar and import it to all sites); delete navbar on index
- style is not consistently applied
- David: users.json ==> users.csv (import pandas); make second login page; remove quotes around names; auto update map somehow
- Madeline: heroku research / add confetti


- sending verification code emails
- changing json to database (and something about images)
- put it onto heroku





#Completed:
- fix upload images/register
- script injections and bad names
- view yearbook msgs not just to Ziyong
- Maps
- sendMessages image ratio/responsiveness
- edit profile bug fixed
- passwords are hashed
- sticky notes (are AWESOMEEEE)

#notCompleted:
- checkmarks next to names
- responsive web design (main)
- notify.js


#TODO 4/20/20
- Alek: fix upload images/register; script injections and bad names; view yearbook msgs not just to Ziyong
- Ziyong: checkmark next to name; sendMessages image ratio; general responsive web design
- David: Maps (allow user to input college destination); general responsive web design
- Leon: generate/hash password; fix bug for edit profile (notification w/ notify.js)
- Andrew: sticky notes in myMessages; general responsive web design

protection against accessing things when not signed in (hope: w/o username/password in url) (Ziyong, Alek ~ Tuesday 9-11pm zoom meeting)

date: wednesday night (9pm)

total end date: saturday 8pm (schedule call w/school ppl to show it off)
release date: may 1st (college decision date)

check: can hack js with single quotes? wrap everything in try/catch statements

#Later
- GoFundMe
- heroku
- convert json to database
- expand to other schools


# TODO 4/17/20
- Leon: TBD
- Joy: TBD
- Ziyong: TBD

- David: main.html, make it look pretty, checks if signed
- Alek: Emails and Maps
- Andrew: Send messages and My Messages

- General To Do's
  - Remove sent messages and add a check next to persons name if signed
  - Make Font's readable and big enough
  - Fix register


# TODO OLD
- Leon: Login/registration
- Joy: send message
- Ziyong: registration page (image input/upload) => work with Leon
- David: main.html
- Alek: database stuff
- Andrew: Front end and make it look cute

### brainstorming

account DB
account interface

account personal information -- where you're going to college

## front end big picture:
  - index.html login/registration page
  - main.html shows a list of people you can click on people to view their profile and
  send them a message
  - sendmessage.html (view someone's profile and send them a message optionally)
  - mymessages.html (view messages that you have received)
  - sentmessages.html (view messages that you have written)

## back end big picture:
  - /login
  - /register
  - /send_message
  - /view_my_messages
  - /view_sent_messages
  - /view_profile
  - /edit_profile

later:
  privacy (accept new account requests)
  security: what about passwords
  pictures
  handwriting font


message DB
message sending interface
later: privacy (accept new account requests)

### registration information
- name (first and last without spaces) => username
- password (make sure not too intense)
- personal email
- description/bio



# old TODO
- Leon: Login/registration
- Joy: send message
- Ziyong: registration page (image input/upload) => work with Leon
- David: main.html
- Alek: database stuff
- Andrew: Front end

## meeting notes:
- leon: have been just messing around with style
- david: drew stuff, messing around
- andrew: we shouldn't we use react, we shuold just make it look good
- alek: yoooo imgsssss  brororoooororororo will enver get old
- joy: sendmesssages lit

## Thursday TODOs:
- {ALEK} once you login, it needs to know who you are logged in as
  - possible solution: username & passwordhash in url
  - better solution: flask session?...
- {leon, david} index.html: login form
- {leon, david} main.html: search bar
- {leon, david} main.html: link to sendmessages.html (with sendto= in url)
- {} sendmessages.html: show bio, shouldn't need to say who you're sending it to
- {} sendmessages.html: dont submit empty messages
- {} sendmessages.html: look better
- {} mymessages.html: should show your messages, and your profile
- {} mymessages.html: edit profile thing
- {} /sendmessages: its kind of broken, e.g. if a user doesnt have an entry in the json already, itll be screwed
- {leon}: /login *hash the passwords* `import hashlib`
- main.html
- {andrew} index.html form style
- {andrew} sendmessages.html form style
- {andrew} sendmessages.html form style
- {andrew} mymessages.html form style
- {ziyong} grid main.html (make it look like a yearbook)
- {ziyong} base.html / style.css (header, footer, other stuff?)
