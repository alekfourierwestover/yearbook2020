from flask import Flask, render_template, request, jsonify, redirect, url_for, session, make_response
from flask_mail import Message, Mail
import json
import io
import csv
from passlib.hash import sha256_crypt
import uuid
import os
import random
from PIL import Image

with open("data/registered_schools.json", "r") as f:
    REGISTERED_SCHOOLS = json.load(f)

with open("data/school_email_patterns.json", "r") as f:
    SCHOOL_EMAIL_PATTERNS = json.load(f)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRETKEY")

app.config.update(
    DEBUG=False,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.environ.get("EMAILUNM"),
    MAIL_PASSWORD=os.environ.get("EMAILPWD")
)
mail = Mail(app)

def safestr(bad_txt):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, bad_txt))

@app.route("/reset_password", methods=("POST",))
def reset_pwd():
    with open(f"data/{session['school']}/users.json", "r") as f:
        data = json.load(f)
    with open(f"data/{session['school']}/passwords.json", "r") as f:
        passwords = json.load(f)
    new_pwd = safestr(str(random.random()))[:8]

    user_name = request.form.get("name")
    if " " not in user_name:
        return redirect(url_for("serve_index", error="full name must contain a space character"))

    first_name, last_name = user_name.split(" ")
    if len(first_name) < 2 or len(last_name) < 2:
        return redirect(url_for("serve_index", error="name_too_short"))
    first_name = first_name[0].upper() + first_name[1:]
    last_name = last_name[0].upper() + last_name[1:]
    user_name = first_name + " " + last_name

    safe_user_name = safestr(user_name)
    if safe_user_name not in data:
        return redirect(url_for("serve_index", error="user_doesnt_exist"))

    data[safe_user_name]["verified"] = True
    passwords[safe_user_name] = sha256_crypt.hash(new_pwd)

    try:
        msg = Message("Password Reset", sender=app.config.get("MAIL_USERNAME"), recipients=[request.form.get("email")])
        msg.html = f"Hey {user_name}, <br>Your new password is <strong>{new_pwd}</strong>.<br>Thanks!"
        mail.send(msg)

        with open(f"data/{session['school']}/users.json", "w") as f:
            json.dump(data, f, indent=4)

        with open(f"data/{session['school']}/passwords.json", "w") as f:
            json.dump(passwords, f, indent=4)

        return redirect(url_for("serve_index", success="password successfully reset"))
    except Exception as e:
        return redirect(url_for("serve_index", error=str(e)))

@app.route('/send_verification_code/', methods=("GET","POST"))
def session_send_verification_code():
    try:
        msg = Message("Verification Code", sender=app.config.get("MAIL_USERNAME"), recipients=[session["email"]])
        msg.html = f"Hey {session['username']}, <br>Thank you for creating an account for the digital bhs yearbook! <br>Your verification code is <strong>{session['verification_code']}</strong>. <br>Please use this to verify your account at <a href='bhsyearbook.tech'>bhsyearbook.tech</a>. <br>You can also verify your account by just clicking on this link: <a href='http://bhsyearbook.tech/check_verification_code?verification={session['verification_code']}'>verify account</a> <br>Thanks!"
        mail.send(msg)
        return redirect(url_for("serve_verify"))
    except Exception as e:
        return redirect(url_for("serve_index", error=str(e)))

@app.route("/check_verification_code", methods=("POST","GET"))
def check_verification_code():
    try:
        if session["loggedin"] and not session["verified"]:
            if request.method=="POST":
                verification_code = request.form.get("verification")
            else:
                verification_code = request.args.get("verification")

            if session["verification_code"] == verification_code:
                session["verified"] = True
                with open(f"data/{session['school']}/users.json", "r") as f:
                    data = json.load(f)
                data[session.get("uuid")]["verified"] = True
                with open(f"data/{session['school']}/users.json", "w") as f:
                    json.dump(data,f, indent=4)
                return redirect(url_for("serve_main"))
            else:
                return redirect(url_for("serve_verified", error="code_wrong"))
        else:
            return redirect(url_for("serve_index"))
    except:
        return redirect(url_for("serve_index"))


@app.route("/get_colleges_csv", methods=("GET",))
def get_colleges_csv():
    with open(f"data/{session['school']}/users.json", "r") as f:
        data = json.load(f)

    names = []
    institutions = []

    for uuid in data:
        if data[uuid]["senior"] and data[uuid]["verified"]:
            if data[uuid]["institution"] in institutions:
                names[institutions.index(data[uuid]["institution"])] += ", " +data[uuid]["name"]
            else:
                names.append(data[uuid]["name"])
                institutions.append(data[uuid]["institution"])

    for i in range(len(names)):
        temp = names[i].split(", ")
        temp.sort(key=lambda x: x.split(" ")[1].lower())
        names[i]= ", ".join(temp)

    names.insert(0, "names")
    institutions.insert(0, "institutions")

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerows(list(zip(*[institutions, names])))

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=colleges.csv"
    output.headers["Content-type"] = "text/csv"
    return output

# session seems to do the trick!!! just cant login multiple users on one device, which is good anyways!!!!
# session is a dictionary that is stored client side as a cookie
@app.route("/get_username", methods=("GET",))
def get_username():
    return session.get("username")

@app.route("/get_uuid", methods=("GET",))
def get_uuid():
    return session.get("uuid")

@app.route("/get_senior", methods=("GET",))
def get_senior():
    return jsonify(session.get("senior"))

# website page routes, note: you must be logged in to view this
@app.route("/")
@app.route("/<string:school>/")
def serve_index(school="belmonthigh"):
    if school not in REGISTERED_SCHOOLS:
        return redirect(url_for("serve_schoolnotfound"))
    if session.get("loggedin"):
        if session.get("verified"):
            return redirect(url_for("serve_main"))
        else:
            return redirect(url_for("serve_verify"))
    else:
        return render_template("index.html")

@app.route("/main")
def serve_main():
    if session.get("loggedin"):
        if session.get("verified"):
            return render_template("main.html")
        else:
            return redirect(url_for("serve_verify"))
    else:
        return redirect(url_for("serve_index"))

@app.route("/mymessages")
def serve_mymessages():
    if session.get("loggedin"):
        if session.get("verified"):
            return render_template("mymessages.html")
        else:
            return redirect(url_for("serve_verify"))
    else:
        return redirect(url_for("serve_index"))

@app.route("/sendmessages")
def serve_sendmessages():
    if session.get("loggedin"):
        if session.get("verified"):
            return render_template("sendmessages.html")
        else:
            return redirect(url_for("serve_verify"))
    else:
        return redirect(url_for("serve_index"))

@app.route("/edit")
def serve_edit():
    if session.get("loggedin"):
        if session.get("verified"):
            return render_template("edit.html")
        else:
            return redirect(url_for("serve_verify"))
    else:
        return redirect(url_for("serve_index"))

@app.route("/schoolnotfound", methods=("GET",))
def serve_schoolnotfound():
    return render_template("schoolnotfound.html")

@app.route("/map")
def serve_map():
    if session.get("loggedin"):
        if session.get("verified"):
            return render_template("map.html")
        else:
            return redirect(url_for("serve_verify"))
    else:
        return redirect(url_for("serve_index"))

@app.route("/verify")
def serve_verify():
    if not session.get("verified"):
        if session.get("loggedin"):
            return render_template("verify.html")
        else:
            return redirect(url_for("serve_index", error="malicious_user"))
    else:
        return redirect(url_for("serve_main"))

# request routes
@app.route("/logout", methods=("POST","GET"))
def handle_logout():
    session["loggedin"] = False
    session["verified"] = False
    session["username"] = ""
    session["uuid"] = ""
    return redirect(url_for("serve_index", school=session.get('school')))

@app.route("/login", methods=("POST",))
@app.route("/<string:school>/login", methods=("POST",))
def handle_login(school="belmonthigh"):
    session["school"] = school
    if school not in REGISTERED_SCHOOLS:
        return redirect(url_for("serve_schoolnotfound"))

    # request.form["key"] extracts a value from the js form
    with open(f"data/{session['school']}/users.json", "r") as f:
        data = json.load(f)
    with open(f"data/{session['school']}/verification_codes.json", "r") as f:
        verification_codes = json.load(f)
    with open(f"data/{session['school']}/passwords.json", "r") as f:
        passwords = json.load(f)

    user_name = request.form.get("name")

    if " " not in user_name:
        return redirect(url_for("serve_index", error="full name must contain a space character"))

    first_name, last_name = user_name.split(" ")
    if len(first_name) < 2 or len(last_name) < 2:
        return redirect(url_for("serve_index", error="name is too short"))
    first_name = first_name[0].upper() + first_name[1:]
    last_name = last_name[0].upper() + last_name[1:]
    user_name = first_name + " " + last_name

    safe_user_name = safestr(user_name)

    if safe_user_name not in data:
        return redirect(url_for("serve_index", error="user doesnt exist"))

    if sha256_crypt.verify(request.form.get("password"), passwords[safe_user_name]):
        session["username"] = user_name
        session["uuid"] = safe_user_name
        session["loggedin"] = True
        session["verified"] = data[safe_user_name]["verified"]
        session["verification_code"] = verification_codes[safe_user_name]
        session["senior"] = data[safe_user_name]["senior"]
        return redirect(url_for("serve_main"))
    else:
        return redirect(url_for("serve_index", error="password wrong"))

@app.route("/register", methods=("POST",))
@app.route("/<string:school>/register", methods=("POST",))
def handle_register(school="belmonthigh"):
    if school not in REGISTERED_SCHOOLS:
        return redirect(url_for("serve_schoolnotfound"))
    print(session.get("school"))

    # request.form["key"] extracts a value from the js form
    with open(f"data/{school}/users.json", "r") as f:
        data = json.load(f)

    first_name = request.form["firstname"].strip()
    last_name = request.form["lastname"].strip()

    if len(last_name) < 2 or len(first_name) < 2:
        return redirect(url_for("serve_index", error="name is too short"))

    if request.form["password"] != request.form["confirm"]:
        return redirect(url_for("serve_index", error="passwords dont match"))

    first_name = first_name[0].upper() + first_name[1:]
    last_name = last_name[0].upper() + last_name[1:]

    user_name = first_name + " " + last_name
    safe_user_name = safestr(user_name)
    user_email = request.form["email"].lower()

    email_good = False
    for possible_email_pattern in SCHOOL_EMAIL_PATTERNS[school]["all"]:
        if possible_email_pattern in user_email:
            email_good = True
            break

    email_is_seniors = False
    for possible_email_pattern in SCHOOL_EMAIL_PATTERNS[school]["senior"]:
        if possible_email_pattern in user_email:
            email_is_seniors = True
            break

    if not email_good:
        return redirect(url_for("serve_index", error="email is no good"))

    if last_name.lower().replace("-", "") not in user_email:
        return redirect(url_for("serve_index", error="email does not contain your lastname"))

    if safe_user_name in data:
        return redirect(url_for("serve_index", error="username taken"))

    session["school"] = school
    session["username"] = user_name
    session["uuid"] = safe_user_name
    session["loggedin"] = True
    session["verified"] = False
    session["email"] = user_email
    session["senior"] = email_is_seniors 
    session["verification_code"] = safestr(str(random.random()))[:8]

    try:
        crop_info = json.loads(request.form.get("crop_info"))
        img_stream = request.files.get("profilepic").stream
        img_file = f"static/pfps/{safe_user_name}.png"
        with open(img_file, "wb") as f:
            f.write(img_stream.read())
        im = Image.open(img_file)
        im_cropped = im.crop([int(p) for p in crop_info["points"]])
        im_cropped.save(img_file, "PNG")

    except:
        pass

    data[safe_user_name] = {
        "name": user_name,
        "email": request.form["email"],
        "institution": request.form["institution"],
        "bio": request.form["bio"],
        "verified": False,
        "senior": session["senior"]
    }
    with open(f"data/{session['school']}/users.json", "w") as f:
        json.dump(data, f, indent=4)

    with open(f"data/{session['school']}/passwords.json", "r") as f:
        passwords = json.load(f)
    passwords[session["uuid"]] = sha256_crypt.hash(request.form["password"])
    with open(f"data/{session['school']}/passwords.json", "w") as f:
        json.dump(passwords, f, indent=4)

    with open(f"data/{session['school']}/verification_codes.json", "r") as f:
        verification_codes = json.load(f)
    verification_codes[session["uuid"]] = session["verification_code"]
    with open(f"data/{session['school']}/verification_codes.json", "w") as f:
        json.dump(verification_codes, f, indent=4)

    session_send_verification_code()
    return redirect(url_for("serve_verify"))

@app.route("/getProfiles", methods=("GET",))
def getProfiles():
    if not(session["loggedin"] and session["verified"]):
        return redirect(url_for("serve_index", error="malicious user"))

    print(session['school'])
    with open(f"data/{session['school']}/users.json", "r") as f:
        data = json.load(f)

    verified_senior_profiles = {}
    for uuid in data:
        if data[uuid]["verified"] and data[uuid]["senior"]:
            verified_senior_profiles[uuid] = data[uuid]

    return jsonify(verified_senior_profiles)

@app.route("/send_message", methods=("POST",))
def handle_send_message():
    try:
        if not (session["loggedin"] and session["verified"]):
            return redirect(url_for("serve_index", error="malicious user"))
        with open(f"data/{session['school']}/messages.json", "r") as f:
            message_data = json.load(f)

        with open(f"data/{session['school']}/users.json", "r") as f:
            user_data = json.load(f)

        sent_from = session.get("username")
        sent_from_uuid = session.get("uuid")
        send_to = request.form.get("sendto")
        message = request.form.get("message")

        if send_to not in user_data.keys():
            session["loggedin"] = False
            return url_for("serve_index", error="malicious user")

        if not send_to in message_data.keys():
            message_data[send_to] = { sent_from: [message] }
        elif sent_from not in message_data[send_to].keys():
            message_data[send_to][sent_from] = [message]
        else:
            message_data[send_to][sent_from].append(message)

        with open(f"data/{session['school']}/messages.json", "w") as f:
            json.dump(message_data, f, indent=4)

        return url_for("serve_main", sent_message="true")
    except:
        return redirect(url_for("serve_index", error="malicious user"))

@app.route("/view_my_messages", methods=("GET",))
def handle_view_my_messages():
    try:
        with open(f"data/{session['school']}/messages.json", "r") as f:
            data = json.load(f)[session.get("uuid")]
        return jsonify(data)
    except:
        return "no messages"

@app.route("/get_registered_schools", methods=("GET",))
def handle_get_registered_schools():
    return jsonify(REGISTERED_SCHOOLS)

@app.route("/get_uuids_sentto", methods=("GET",))
def handle_get_uuids_sentto():
    if not (session["loggedin"] and session["verified"]):
        return redirect(url_for("serve_index", error="malicious user"))

    with open(f"data/{session['school']}/messages.json", "r") as f:
        data = json.load(f)

    uuids_sentto = []
    for uuid_sentto in data:
        if session["username"] in data[uuid_sentto]:
            uuids_sentto.append(uuid_sentto)

    return jsonify(uuids_sentto)

@app.route("/view_profile", methods=("GET",))
# returns name and bio
def handle_view_profile():
    if not (session["loggedin"] and session["verified"]):
        return redirect(url_for("serve_index", error="malicious user"))
    try:
        with open(f"data/{session['school']}/users.json", "r") as f:
            data = json.load(f)
            return jsonify(data[request.args.get("uuid")])
    except:
        return redirect(url_for("serve_index", error="malicious user"))

@app.route("/edit_password", methods=("POST", ))
def handle_edit_password():
    if not (session["loggedin"] and session["verified"]):
        return redirect(url_for("serve_index", error="malicious user"))
    with open(f"data/{session['school']}/passwords.json", "r") as f:
        passwords = json.load(f)

    try:
        if sha256_crypt.verify(request.form.get("password"), passwords[session.get("uuid")]):
            passwords[session.get("uuid")] = sha256_crypt.hash(request.form.get("newpassword"))
            with open(f"data/{session['school']}/passwords.json", "w") as f:
                json.dump(passwords, f, indent = 4)
                return redirect(url_for("serve_main"))
        else:
            return redirect(url_for("serve_edit", error="password wrong"))
    except:
        session["loggedin"] = False
        session["verified"] = False
        return redirect(url_for("serve_index", error="error"))

@app.route("/edit_quote", methods=("POST", ))
def handle_edit_quote():
    if not (session["loggedin"] and session["verified"]):
        return redirect(url_for("serve_index", error="malicious user"))
    with open(f"data/{session['school']}/users.json", "r") as f:
        data = json.load(f)
    with open(f"data/{session['school']}/passwords.json", "r") as f:
        passwords = json.load(f)
    try:
        quote = request.form.get("quote")
        if sha256_crypt.verify(request.form.get("password"), passwords[session.get("uuid")]):
            data[session.get("uuid")]["bio"] = quote
            with open(f"data/{session['school']}/users.json", "w") as f:
                json.dump(data, f, indent = 4)
                return redirect(url_for("serve_main"))
        else:
            return redirect(url_for("serve_edit", error="password wrong"))
    except:
        session["loggedin"] = False
        session["verified"] = False
        return redirect(url_for("serve_index", error="user not found"))

@app.route("/edit_picture", methods=("POST", ))
def handle_edit_picture():
    if not (session["loggedin"] and session["verified"]):
        return redirect(url_for("serve_index", error="malicious user"))
    with open(f"data/{session['school']}/users.json", "r") as f:
        data = json.load(f)
    with open(f"data/{session['school']}/passwords.json", "r") as f:
        passwords = json.load(f)

    try:
        if sha256_crypt.verify(request.form.get("password"), passwords[session.get("uuid")]):
            try:
                crop_info = json.loads(request.form.get("crop_info"))
                img_stream = request.files.get("profilepic").stream
                img_file = f"static/pfps/{session.get('uuid')}.png"
                with open(img_file, "wb") as f:
                    f.write(img_stream.read())
                im = Image.open(img_file)
                im_cropped = im.crop([int(x) for x in crop_info["points"]])
                im_cropped.save(img_file, "PNG")
            except:
                pass

            return redirect(url_for("serve_main"))
        else:
            return redirect(url_for("serve_edit", error="password wrong"))
    except:
        session["loggedin"] = False
        session["verified"] = False
        return redirect(url_for("serve_index", error="user not found"))

@app.route("/edit_college", methods=("POST", ))
def handle_edit_college():
    if not (session["loggedin"] and session["verified"]):
        return redirect(url_for("serve_index", error="malicious user"))
    with open(f"data/{session['school']}/users.json", "r") as f:
        data = json.load(f)
    with open(f"data/{session['school']}/passwords.json", "r") as f:
        passwords = json.load(f)
    try:
        college = request.form.get("institution")
        if sha256_crypt.verify(request.form.get("password"), passwords[session.get("uuid")]):
            data[session.get("uuid")]["institution"] = college
            with open(f"data/{session['school']}/users.json", "w") as f:
                json.dump(data, f, indent = 4)
                return redirect(url_for("serve_main"))
        else:
            return redirect(url_for("serve_edit", error="password wrong"))
    except:
        session["loggedin"] = False
        session["verified"] = False
        return redirect(url_for("serve_index", error="user not found"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port='80', debug=True)

