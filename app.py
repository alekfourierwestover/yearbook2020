from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, current_user, login_user
import json

app = Flask(__name__)
login = LoginManager(app)

@login.user_loader
def load_user(id):
    with open("users.json", "r") as f:
        data = json.load(f)
        return jsonify(data[id])

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
    #serves website
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
    with open("users.json", "r") as f:
        x = json.load(f)
        user_name = request.form["name"]

        img_stream = request.files.get("profilepic").stream
        with open(f"static/pfps/{user_name}.png", "wb") as f: # make sure usernames dont have werid stuff
            f.write(img_stream.read())

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
        data = json.load(f)
        try:
            data[request.form.get("send to")][request.form.get("from")].append(request.form.get("message"))
        except:
            data[request.form.get("send to")][request.form.get("from")] = [request.form.get("message")]
    with open("messages.json", "w") as f:
        json.dump(data, f, indent=4)

    return redirect(url_for("serve_main"))



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
    try:
        user_name = request.args.get("name")
    except:
        return "user not found"
    with open("users.json", "r") as f:
        data = json.load(f)
        return jsonify(data[user_name])

@app.route("/edit_profile")
def handle_edit_profile():
    return ""

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
