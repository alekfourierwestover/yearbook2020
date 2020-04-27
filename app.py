from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_mail import Message, Mail
import json
from passlib.hash import sha256_crypt
import uuid
import os
import random

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

@app.route('/send_verification_code/', methods=("GET",))
def session_send_verification_code():
    try:
        msg = Message("Verification Code", sender=app.config.get("MAIL_USERNAME"), recipients=[session["email"]])
        msg.body = f"Hey {session['username'], \nThank you for creating an account on the bhsyearbook.tech website. You're verification code is {session['verification_code']}. Please use this at <a href='bhsyearbook.tech/verify'>bhsyearbook.tech/verify</a>"
        mail.send(msg)
        return 'Mail sent!'
    except Exception as e:
        return str(e)

# session seems to do the trick!!! just cant login multiple users on one device, which is good anyways!!!!
# session is a dictionary that is stored client side as a cookie
@app.route("/get_username", methods=("GET",))
def get_username():
    return session.get("username")

@app.route("/get_uuid", methods=("GET",))
def get_uuid():
    return session.get("uuid")

# website page routes, note: you must be logged in to view this
@app.route("/index")
@app.route("/")
def serve_index():
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
            return redirect(url_for("serve_main"))
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

@app.route("/map")
def serve_map():
    if session.get("loggedin"):
        if session.get("verified"):
            return render_template("map.html")
        else:
            return redirect(url_for("serve_verify"))
    else:
        return redirect(url_for("serve_index"))

# request routes
@app.route("/logout", methods=("POST","GET"))
def handle_logout():
    session["loggedin"] = False
    session["verified"] = False
    session["username"] = ""
    session["uuid"] = ""
    return redirect(url_for("serve_index"))

@app.route("/login", methods=("POST",))
def handle_login():
    # request.form["key"] extracts a value from the js form
    with open("users.json", "r") as f:
        data = json.load(f)
        user_name = request.form.get("name").lower()

        tmp = user_name.split(" ")
        for leon in range(len(tmp)):
            tmp[leon] = tmp[leon][0].upper() + tmp[leon][1:]
        user_name = " ".join(tmp)


        safe_user_name = safestr(user_name)
        try:
            if sha256_crypt.verify(request.form.get("password"), data[safe_user_name]["password"]):
                session["username"] = user_name
                session["uuid"] = safe_user_name
                session["loggedin"] = True
                session["verified"] = data[safe_user_name]["verified"]
                session["verification_code"] = data[safe_user_name]["verification_code"]
                return redirect(url_for("serve_main"))
            else:
                return redirect(url_for("serve_index", error="password_wrong"))
        except:
            return redirect(url_for("serve_index", error="user_not_found"))

@app.route("/register", methods=("POST",))
def handle_register():
    # request.form["key"] extracts a value from the js form
    with open("users.json", "r") as f:
        x = json.load(f)
        user_name = request.form["name"].lower()
        
        tmp = user_name.split(" ")
        for leon in range(len(tmp)):
            tmp[leon] = tmp[leon][0].upper() + tmp[leon][1:]
        user_name = " ".join(tmp)

        safe_user_name = safestr(user_name)
        session["username"] = user_name
        session["uuid"] = safe_user_name
        session["loggedin"] = True
        session["verified"] = False
        session["email"] = request.form["email"]
        session["verification_code"] = safestr(str(random.random()))

        try:
            img_stream = request.files.get("profilepic").stream
            with open(f"static/pfps/{safe_user_name}.png", "wb") as f:
                f.write(img_stream.read())
        except:
            pass

        x[safe_user_name] = {
            "name": user_name,
            "email": request.form["email"],
            "password": sha256_crypt.hash(request.form["password"]),
            "institution": request.form["institution"],
            "bio": request.form["bio"],
            "verified": False,
            "verification_code": session["verification_code"]
        }
        with open("users.json", "w") as f:
            json.dump(x, f, indent = 4)

        session_send_verification_code()
        return redirect(url_for("serve_verify"))

@app.route("/getProfiles", methods=("GET",))
def getProfiles():
    with open("users.json", "r") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/send_message", methods=("POST",))
def handle_send_message():
    with open("messages.json", "r") as f:
        message_data = json.load(f)

    with open("users.json", "r") as f:
        user_data = json.load(f)

    sent_from = session.get("username")
    sent_from_uuid = session.get("uuid")
    send_to = request.form.get("sendto")
    message = request.form.get("message")

    if send_to not in user_data.keys():
        session["loggedin"] = False
        return url_for("serve_index", error="malicious_user")

    if not send_to in message_data.keys():
        message_data[send_to] = { sent_from: [message] }
    elif sent_from not in message_data[send_to].keys():
        message_data[send_to][sent_from] = [message]
    else:
        message_data[send_to][sent_from].append(message)

    with open("messages.json", "w") as f:
        json.dump(message_data, f, indent=4)

    return url_for("serve_main")


@app.route("/view_my_messages", methods=("GET",))
def handle_view_my_messages():
    try:
        with open("messages.json", "r") as f:
            data = json.load(f)[session.get("uuid")]
        return jsonify(data)
    except:
        return "no messages"

@app.route("/view_all_messages", methods=("GET",))
def handle_view_all_messages():
    try:
        with open("messages.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except:
        return "no messages"

@app.route("/view_profile", methods=("GET",))
# returns name and bio
def handle_view_profile():
    with open("users.json", "r") as f:
        data = json.load(f)
        return jsonify(data[request.args.get("uuid")])

@app.route("/edit_password", methods=("POST", ))
def handle_edit_password():
    with open("users.json", "r") as f:
        data = json.load(f)

    try:
        if sha256_crypt.verify(request.form.get("password"), data[session.get("uuid")]["password"]):
            data[session.get("uuid")]["password"] = sha256_crypt.hash(request.form.get("newpassword"))
            with open("users.json", "w") as f:
                json.dump(data, f, indent = 4)
                return redirect(url_for("serve_main"))
        else:
            session["loggedin"] = False
            return redirect(url_for("serve_index", error="password_wrong"))
    except:
        return redirect(url_for("serve_index", error="error"))

@app.route("/edit_quote", methods=("POST", ))
def handle_edit_quote():
    with open("users.json", "r") as f:
        data = json.load(f)
    try:
        quote = request.form.get("quote")
        if sha256_crypt.verify(request.form.get("password"), data[session.get("uuid")]["password"]):
            data[session.get("uuid")]["bio"] = quote
            with open("users.json", "w") as f:
                json.dump(data, f, indent = 4)
                return redirect(url_for("serve_main"))
        else:
            session["loggedin"] = False
            return redirect(url_for("serve_index", error="password_wrong"))
    except:
        return redirect(url_for("serve_index", error="user_not_found"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port='80')

