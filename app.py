from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/sendmessage", methods=["POST", "GET"])
def send_message():
    if request.method == "POST":
        message = request.form["message"]
        sendTo = request.form["sendTo"]
        return redirect(url_for("sentmessages", usr=message))
    else:
        return render_template('sendmessage.html')

@app.route("/<usr>")
def sentmessages(usr):
    return f"<p>{usr}</p>"

if __name__=="__main__":
    app.run(debug = True)
