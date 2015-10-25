import os
from flask import Flask, render_template, redirect, request
from urllib import urlencode

app = Flask(__name__)

app.secret_key = "a_very_dumb_secret"

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]

@app.route("/")
def index_page():
    """Initial landing page"""

    params = {"client_id": client_id, "redirect_uri": "http://localhost:5000/slacked"}

    oauth_url = "https://slack.com/oauth/authorize?" + urlencode(params)

    return redirect(oauth_url)


@app.route("/slacked")
def slacked():
    """Landing page for authorized slack users"""



    return effort


if __name__ == '__main__':
    print "Server up and running, yo!"
    app.run()
