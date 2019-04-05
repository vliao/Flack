import os

from flask import Flask, jsonify, request, render_template, session
from flask_socketio import SocketIO, emit
from flask_session import Session


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)

channels:set = {"generalChat"}
user = ''

@app.route("/")
def index():
    if session["user"] is None:
        return render_template("index.html")
    else: 
        return render_template("welcome.html", user=session["user"], channels=channels)

@socketio.on("sign in")
def signIn(data):
    user = data["user"]
    emit("sign in", {"user":user}, broadcast=True)

@app.route("/welcome", methods=["get"])
def showChatRoom():
    session["user"] = request.args.get("user")
    return render_template("welcome.html", user=session["user"], channels=channels)

@app.route("/chatRoom", methods=["POST"])
def updateChannelList():
    newChannel = request.form.get("channelName")
    channels.add(newChannel)
    return render_template("welcome.html", user=session["user"], channels=channels)

# route to any channel.
# maybe all channels should use the same html though, just serve up different chat histories?
@app.route("/<channel>")
def goToChannel(channel):
    return render_template(f"{channel}.html")


