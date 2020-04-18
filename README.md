# yearbook2020
Yearbook for BHS 2020 :(

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
  - 


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
