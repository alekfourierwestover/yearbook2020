from flask import Flask, render_template, request, jsonify, redirect, url_for
from pandas as pd
import json

app = Flask(__name__)

# website page routes
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
    return render_template("sendmessages.html")

@app.route("/sentmessages")
def serve_sentmessages():
    return render_template("sentmessages.html")

# request routes
@app.route("/login", methods=("POST",))
def handle_login():
    # request.form["key"] extracts a value from the js form
    with open("user.json", "r") as f:
        data = json.load(f)
        email = request.args.get("email")
        password = request.args.get("password")

        try:
            if password == data[email]["password"]:
                return redirect(url_for("serve_main"))
            else:
                return "Your email and password do not match. Please try again!"
        except:
                return "There is no such account. Try making an account!"



@app.route("/register", methods=("POST",))
def handle_register():
    # request.form["key"] extracts a value from the js form
    with open("register.json", "r") as f:
        x = json.load(f)
        img_stream = request.files.get("profilepic").stream
        x.append({
            "name": request.form["name"],
            "email": request.form["email"],
            "password": request.form["password"],  # UM THIS IS A SUPER HUGE SECURITY ISSUE
            "bio": request.form["bio"],
            "profilepic": str(img_stream.read())
        })
        with open("register.json", "w") as f:
            json.dump(x, f, indent = 4)
        return "Thanks " + request.form["name"]

@app.route("/getProfiles", methods=("GET",))
def getProfiles():
    with open("register.json", "r") as f:
        data = json.load(f)
    return jsonify(data)


@app.route("/send_message", methods=("POST",))
def handle_send_message():
    # request.form["key"] extracts a value from the js form
    return ""

@app.route("/view_my_messages", methods=("GET",))
def handle_view_my_messages():
    return ""

@app.route("/view_sent_messages")
def handle_view_sent_messages():
    return ""

# returns name and bio
@app.route("/view_profile")
def handle_view_profile():
    return ""

@app.route("/edit_profile")
def handle_edit_profile():
    return ""

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
