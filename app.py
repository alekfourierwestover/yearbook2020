from flask import Flask, render_template, request, jsonify, redirect, url_for
import json

app = Flask(__name__)

# website page routes
@app.route("/index")
@app.route("/")
def serve_index():
    return render_template("index.html")

@app.route("/base")
def serve_base():
    return render_template("base.html")

@app.route("/main")
def serve_main():
    return render_template("main.html")

@app.route("/mymessages")
def serve_mymessages():
    return render_template("mymessages.html")

@app.route("/sendmessages")
def serve_sendmessages():
    #serves website
    return render_template("sendmessages.html")

@app.route("/sentmessages")
def serve_sentmessages():
    return render_template("sentmessages.html")

# request routes
@app.route("/login", methods=("POST",))
def handle_login():
    # request.form["key"] extracts a value from the js form
    with open("users.json", "r") as f:
        data = json.load(f)
        name = request.form.get("name")
        password = request.form.get("password")
        try:
            if password == data[name]["password"]:
                return redirect(url_for("serve_main", name=name, password=password))
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

        try:
            img_stream = request.files.get("profilepic").stream
            with open(f"static/pfps/{user_name}.png", "wb") as f: # make sure usernames dont have werid stuff
                f.write(img_stream.read())
        except:
            pass

        x[user_name] = {
            "name": user_name,
            "email": request.form["email"],
            "password": request.form["password"],  # UM THIS IS A SUPER HUGE SECURITY ISSUE
            "bio": request.form["bio"]
        }
        with open("users.json", "w") as f:
            json.dump(x, f, indent = 4)
        # return "Thanks " + user_name

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

    sent_from = request.form.get("name") 
    password = request.form.get("password") 
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
    with open("messages.json", "r") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/view_sent_messages")
def handle_view_sent_messages():
    # request.args.get("name")
    return ""

@app.route("/view_profile", methods=("GET",))
# returns name and bio
def handle_view_profile():
    user_name = request.args.get("name")
    with open("users.json", "r") as f:
        data = json.load(f)
        print(data)
        return jsonify(data[user_name])

@app.route("/edit_profile")
def handle_edit_profile():
    return ""

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
