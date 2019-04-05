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

# channels:set = {"generalChat"}
# messages = ["vivian:hello"]
maxMessages = 3
messages:dict = {"generalChat":["jenn:hey"], "a":[]}
channels = messages.keys()

@app.route("/")
def index():
    if session["user"] is None:
        return render_template("index.html")
    else: 
        return render_template("welcome.html", user=session["user"], channels=channels)

@app.route("/welcome", methods=["get"])
def showChatRoom():
    session["user"] = request.args.get("user")
    return render_template("welcome.html", user=session["user"], channels=channels)

@app.route("/chatRoom", methods=["POST"])
def updateChannelList():
    newChannel = request.form.get("channelName")
    messages[newChannel] = []
    # channels.add(newChannel)
    return render_template("welcome.html", user=session["user"], channels=channels)

# route to any channel.
# maybe all channels should use the same html though, just serve up different chat histories?
@app.route("/<channel>")
def goToChannel(channel):
    channel = channel
    return render_template(f"generalChat.html", channel=channel, messages=messages[channel][maxMessages:])


#save messages
@socketio.on("send message")
def addMessage(data):
    user=session["user"]
    message = user+":"+data["message"]
    channel = data["channel"]
    messages[channel].append(message)
    emit("update messages", {"message":message}, broadcast=True)