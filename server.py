import os, random, string, requests, json
from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from urllib import urlencode, urlopen
import re


app = Flask(__name__)

app.secret_key = "a_very_dumb_secret"

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
MYEMAIL = os.environ["MYEMAIL"]
state = None


@app.route("/")
def index_page():
    """Initial landing page"""

    global state
    state = randomWord()

    params = {"client_id": CLIENT_ID,
                "redirect_uri": "http://localhost:5000/slacked",
                "state": state,
                "team": "Dovetail"}

    oauth_url = "https://slack.com/oauth/authorize?" + urlencode(params)

    return redirect(oauth_url)


@app.route("/slacked")
def slacked():
    """Landing page for authorized slack users"""


    state_returned = request.args.get("state")
    client_code = request.args.get("code")

    if check_state(state_returned) is False:
        return "Slack did not return the expected state variable! You've been h4x0r3d."
    else:
        # OAuth parameters
        params = {"client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "code": client_code}

        oauth_url = "https://slack.com/api/oauth.access?" + urlencode(params)
        json_response = requests.get(oauth_url)

        # parse json response
        response = json_response.json()
        # identify user
        user_token = response["access_token"]
        # get list of channels for user
        channel_list = get_channel_list(user_token)

        # test: get history for one channel, print it out
        first_channel = channel_list[0]
        first_channel_history = get_channel_history(user_token, first_channel)
        
        # print first_channel_history

        msg_dictionary = make_history_dictionary(first_channel_history)

        test_dict = {"data": [{"text": "I love Titanic."}, 
                    {"text": "I hate Titanic."}]}
        sentiment = get_sentiment(test_dict)

        print sentiment

        # for message in first_channel_history:
        #     print "\n\n", message

    return "authorized"


##################### Helper functions

def randomWord():
    """Generates a random 10 character string, to use as an API verification"""
    return ''.join(random.choice(string.lowercase) for i in range(10))


def check_state(state_returned):
    """Checks that state sent to Slack is correctly returned."""

    if state_returned != state:
        raise Exception("Slack did not return the expected state variable! You've been h4x0r3d.")
        return False
    else:
        return True


def get_channel_list(token):
    """Give a user token, returns a list of tuples with active channel names and ids"""

    channel_params = {"token": token, "exclude_archived": 1}
    channel_url = "https://slack.com/api/channels.list?" + urlencode(channel_params)
    json_channel = requests.get(channel_url)
    channel_response = json_channel.json()

    channel_list = []
    
    for channel in channel_response["channels"]:
        channel_tuple = (channel["name"], channel["id"])
        channel_list.append(channel_tuple)

    return channel_list


def get_channel_history(token, channel_tuple):
    """Given a channel tuple, returns history of the channel"""

    history_params = {"token": token, 
                        "channel": channel_tuple[1],
                        "inclusive": 1,
                        "count":30
                        }
    history_url = "https://slack.com/api/channels.history?" + urlencode(history_params)
    json_history = requests.get(history_url)
    history_response = json_history.json()

    msg_list = []

    for msg in history_response["messages"]:
        msg_list.append(msg["text"])

    return msg_list

def make_history_dictionary(msg_list):
    """Converts a message list into a dictionary for sentiment analysis"""

    # dictionary = {"data":[
                        # {"text": "I love Titanic."}, 
                        # {"text": "I hate Titanic."}
                        # ]}

    msg_dictionary = {}
    msg_text_list = []

    for msg in msg_list:
        msg_dict = {}
        msg = clean_msg(msg)
        msg_dict["text"] = msg
        msg_text_list.append(msg_dict)

    msg_dictionary["data"] = msg_text_list

    return msg_dictionary

def clean_msg(msg):
    """Takes single message, removes user tags and links, returns stripped message"""

    # things to remove: <xxx>

    cleaned_msg = re.sub("[<].*?[>]", "", msg)

    return cleaned_msg

def get_sentiment(msg_dictionary):
    """Given a message dictionary, makes an API call to Sentiment140 to get sentiments"""

    msg_dictionary["appid"] = MYEMAIL
    sentiment_data = json.dumps(msg_dictionary)

    sentiment_api_call = urlopen('http://www.sentiment140.com/api/bulkClassifyJson', sentiment_data)
    sentiment_response = sentiment_api_call.read()
     
    return sentiment_response


# copied a test dictionary from the sentiment140 site, and am using that to test the api call. 
# getting a 405 - method not allowed
test_dict = {"data": [{"text": "I love Titanic."}, 
                    {"text": "I hate Titanic."}]}

sentiment = get_sentiment(test_dict)
print sentiment



if __name__ == '__main__':
    app.run(debug=True)
