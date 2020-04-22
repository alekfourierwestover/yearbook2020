from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
from passlib.hash import sha256_crypt
import uuid

app = Flask(__name__)

def safestr(bad_txt):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, bad_txt))

# seems to do the trick!!! just cant login multiple users on one device, which is good anyways!!!!
@app.route("/get_username", methods=("GET",))
def get_username():
    return session.get("username")

@app.route("/get_uuid", methods=("GET",))
def get_uuid():
    return safestr(session.get("username"))

# website page routes, note: you must be logged in to view this
@app.route("/index")
@app.route("/")
def serve_index():
    if session.get("loggedin"):
        return redirect(url_for("serve_main"))
    else:
        return render_template("index.html")

@app.route("/main")
def serve_main():
    if session.get("loggedin"):
        return render_template("main.html")
    else:
        return redirect(url_for("serve_index"))

@app.route("/mymessages")
def serve_mymessages():
    if session.get("loggedin"):
        return render_template("mymessages.html")
    else:
        return redirect(url_for("serve_index"))

@app.route("/sendmessages")
def serve_sendmessages():
    if session.get("loggedin"):
        return render_template("sendmessages.html")
    else:
        return redirect(url_for("serve_index"))

@app.route("/edit")
def serve_edit():
    if session.get("loggedin"):
        return render_template("edit.html")
    else:
        return redirect(url_for("serve_index"))

@app.route("/map")
def serve_map():
    if session.get("loggedin"):
        return render_template("map.html")
    else:
        return redirect(url_for("serve_index"))

# request routes
@app.route("/logout", methods=("POST",))
def handle_logout():
    session["loggedin"] = False
    session["username"] = ""
    return redirect(url_for("serve_index"))

@app.route("/login", methods=("POST",))
def handle_login():
    # request.form["key"] extracts a value from the js form
    with open("users.json", "r") as f:
        data = json.load(f)
        name = request.form.get("name")
        safename = safestr(name)
        try:
            if sha256_crypt.verify(request.form.get("password"), data[safename]["password"]):
                session["username"] = name
                session["loggedin"] = True
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
        user_name = request.form["name"]
        session["username"] = user_name
        session["loggedin"] = True
        safe_user_name = safestr(user_name)

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
            "bio": request.form["bio"]
        }
        with open("users.json", "w") as f:
            json.dump(x, f, indent = 4)

        return redirect(url_for("serve_main"))

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
    send_to = request.form.get("sendto")
    message = request.form.get("message")

    if sent_from not in user_data.keys():
        return url_for("serve_index", error="malicious_user")
    if send_to not in user_data.keys():
        return url_for("serve_index", error="malicious_user")
    if user_data[sent_from]["password"] != password:
        return url_for("serve_index", error="malicious_user")

    if not send_to in message_data.keys():
        message_data[send_to] = { sent_from: [message] }
    elif sent_from not in message_data[send_to].keys():
        message_data[send_to][sent_from] = [message]
    else:
        message_data[send_to][sent_from].append(message)

    with open("messages.json", "w") as f:
        json.dump(message_data, f, indent=4)

    return url_for("serve_main", name=sent_from, password=password)


@app.route("/view_my_messages", methods=("GET",))
def handle_view_my_messages():
    try:
        with open("messages.json", "r") as f:
            data = json.load(f)[session.get("username")]
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
        return jsonify(data[request.args.get("name")])

@app.route("/edit_profile", methods=("POST", ))
def handle_edit_profile():
    try:
        with open("users.json", "r") as f:
            data = json.load(f)
            user_name = session.get("username")
            safe_user_name = safestr(user_name)

        if sha256_crypt.verify(request.form["password"], data[safestr(user_name)]["password"]):
            data[safe_user_name]["password"] = sha256_crypt.hash(request.form["newpassword"])
            data[safe_user_name]["bio"] = request.form["quote"]

            with open("users.json", "w") as f:
                json.dump(data, f, indent = 4)
            return redirect(url_for("serve_main"))
        else:
            return redirect(url_for("serve_index", error="password_wrong"))
    except:
        return redirect(url_for("serve_index", error="user_not_found"))

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(debug=True, host='0.0.0.0')

    # ok so looks like session is a dictionary that is stored client side as a cookie
    # testable by going to 192.168.1.165:5000 on your phone and computer simultaneusly; should also be compatible with port forwarding

