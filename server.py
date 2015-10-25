import os, random, string
from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from urllib import urlencode


app = Flask(__name__)

app.secret_key = "a_very_dumb_secret"

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]

@app.route("/")
def index_page():
    """Initial landing page"""



    params = {"client_id": client_id,
                "redirect_uri": "http://localhost:5000/slacked",
                "state": randomWord()}

    oauth_url = "https://slack.com/oauth/authorize?" + urlencode(params)

    return redirect(oauth_url)


@app.route("/slacked")
def slacked():
    """Landing page for authorized slack users"""

    effort = "Successful!"

    return effort


# Helper functions

def randomWord():
    """Generates a random string, to use as an API verification"""
    return ''.join(random.choice(string.lowercase) for i in range(10))


if __name__ == '__main__':
    print "Server up and running, yo!"
    app.run()
