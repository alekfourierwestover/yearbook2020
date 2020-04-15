from flask import Flask, render_template, request, jsonify
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
    return ""

@app.route("/register", methods=("POST",))
def handle_register():
    # request.form["key"] extracts a value from the js form
    __import__('ipdb').set_trace()
    with open("register.json", "r") as f:
        x = json.load(f)
        x.append({
            "name": request.form["name"], 
            "email": request.form["email"], 
            "password": request.form["password"],  # UM THIS IS A SUPER HUGE SECURITY ISSUE 
            "bio": request.form["bio"],
            "profilepic": request.form["profilepic"]
        })
        print(x)
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

@app.route("/view_profile")
def handle_view_profile():
    return ""

@app.route("/edit_profile")
def handle_edit_profile():
    return ""

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
