import os, random, string, requests, json
from flask import Flask, render_template, redirect, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from urllib import urlencode, urlopen
import re
# from channel import Channel
from time import time


app = Flask(__name__)

app.secret_key = "a_very_dumb_secret"

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
MYEMAIL = os.environ["MYEMAIL"]
state = None
channel_tuple_list = []


@app.route("/")
def index_page():
    """Initial landing page"""

    global state
    state = randomWord()

    params = {"client_id": CLIENT_ID,
                "redirect_uri": "http://localhost:5000/slacked",
                "scope": "channels:history channels:read",
                "state": state}

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
        params = {"client_id": CLIENT_ID.strip(),
                    "client_secret": CLIENT_SECRET.strip(), # was having issue with a \r, can't find it :(
                    "code": client_code}

        oauth_url = "https://slack.com/api/oauth.access?" + urlencode(params)       

        json_response = requests.get(oauth_url)
        # parse json response
        response = json_response.json()
        
        # identify user
        print response
        user_token = response["access_token"]

        # get list of channels for user
        channel_list = get_channel_list(user_token)

        for channel in channel_list:
            # print "*****************", channel
            # print "getting channel history:"
            channel_history = get_channel_history(user_token, channel)
            # print channel_history
            # print "getting msg dict:"
            msg_dictionary = make_history_dictionary(channel_history)
            # print "getting sent dict:"
            sentiment_dict = get_sentiment(msg_dictionary)
            # print "getting sent list:"
            sentiment_list = make_sentiment_list(sentiment_dict)
            # print sentiment_list
            # print "getting sent tup:"
            sentiment_tuple = process_sentiment_list(sentiment_list)

            # I know this is terrible...

            channel_tuple = (channel[0], sentiment_tuple[0], sentiment_tuple[1])
            channel_tuple_list.append(channel_tuple)
            # print channel_tuple

    # should probably redirect to route that builds channel objects, pass user token
    # this way refreshing graph can be separated from login
    # return redirect("/bubblebuilder.json", user_token=user_token)
    # print channel_tuple_list
    return redirect("/bubble")


# @app.route("/bubblebuilder.json")
# def build_bubbles():
#     """Gets channel history and builds bubble json"""

    # user_token = get the id from the post request

    # get channel list, using user token

    # for channel, 
        # build objects?
        # get channel history
        # add to objects

    # return json for d3 


@app.route("/channel_data.json")
def make_channel_data():
    """Parses list of channel tups into json for d3 bubble chart"""

    channel_data = {"name": "channels",
                    "children": []
                    }

    for channel in channel_tuple_list:
        channel_dict = {}

        if channel[1] > 0:

            channel_dict["name"] = channel[0]
            channel_dict["value"] = channel[1]
            channel_dict["sentiment"] = channel[2]

            channel_data["children"].append(channel_dict)

    return jsonify(channel_data)


@app.route("/bubble")
def bubble():
    """d3 test run"""

    return render_template("bubble.html")


# @app.route("/cats.json")
# def send_cats():
#     """Test route for building d3 bubble chart"""

#     cats = {"name": "cats",
#             "children": [
#             {"name": "Guido", "value": 160, "color": "black", "sentiment": 1.25},
#             {"name": "Darwin", "value": 110, "color": "chocolate", "sentiment": 2.4},
#             {"name": "Mika", "value": 100, "color": "black", "sentiment": 4},
#             {"name": "Kitin", "value": 150, "color": "orange", "sentiment": -1},
#             {"name": "Pirate Jack", "value": 180, "color": "saddlebrown", "sentiment": 0.25}
#             ]}

#     return jsonify(cats)
   


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
        """Returns history of the channel"""

        ONE_WEEK_SEC = 604800
        epoch_time = time()
        one_week_ago = epoch_time - ONE_WEEK_SEC

        history_params = {"token": token, 
                            "channel": channel_tuple[1],
                            "inclusive": 1,
                            # "count":100
                            "oldest": one_week_ago
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
    #                     {"text": "I love Titanic."}, 
    #                     {"text": "I hate Titanic."}
    #                     ]}

    msg_dictionary = {}
    msg_text_list = []
    skip_msg_list = [" has joined the channel", " has left the channel"]

    for msg in msg_list:
        msg_dict = {}
        msg = clean_msg(msg)

        if msg in skip_msg_list:
            continue
        else:
            msg_dict["text"] = msg
            msg_text_list.append(msg_dict)

    msg_dictionary["data"] = msg_text_list

    return msg_dictionary


def clean_msg(msg):
    """Takes single message, removes user tags and links, returns stripped message"""

    # things to remove: <usernames> <links...> emoticons?!

    stripped_msg = re.sub("[<].*?[>]", "", msg)

    # nope. decoding unicode not supported (it's already unicode)
    # cleaned_msg = unicode(stripped_msg, errors='ignore')

    # cleaned_msg = stripped_msg.encode("utf-8")

    cleaned_msg = stripped_msg

    return cleaned_msg


def get_sentiment(msg_dictionary):
    """Given a message dictionary, makes an API call to Sentiment140 to get sentiments"""

    # add my email to the call, as requested by Sentiment140
    msg_dictionary["appid"] = MYEMAIL
    # convert to json
    sentiment_data = json.dumps(msg_dictionary)

    sentiment_api_call = urlopen('http://www.sentiment140.com/api/bulkClassifyJson', sentiment_data)
    sentiment_response = sentiment_api_call.read()
    # convert to python dictionary
    # ignores character like emoticons which were throwinf unicode errors
    sentiment_response_dict = json.loads(sentiment_response.decode("utf-8","ignore"))
     
    return sentiment_response_dict


def make_sentiment_list(sentiment_dict):
    """Given the sentiment response dictionary, makes list of just the sentiment values"""

    sentiment_list = []

    for sentiment in sentiment_dict["data"]:
        sentiment_list.append(sentiment["polarity"])

    return sentiment_list


def process_sentiment_list(sentiment_list):
    """Given a sentiment list, returns a tuple of length and avg value"""

    if sentiment_list:
        sentiment_tuple = (len(sentiment_list), (float(sum(sentiment_list)) / len(sentiment_list)))
    else:
        sentiment_tuple = (0, 0.0)

    return sentiment_tuple


# new_response = {"data":[
#                     {"text":" has joined the channel","polarity":2,"meta":{"language":"en"}},
#                     {"text":"awww!","polarity":2,"meta":{"language":"en"}},
#                     {"text":"Thank you!  I was pretty proud of myself.","polarity":2,"meta":{"language":"en"}},
#                     {"text":"Awwwww","polarity":2,"meta":{"language":"en"}},
#                     {"text":"is that a stencil ? awesome!","polarity":4,"meta":{"language":"en"}}
#                     ],
#                 "appid":"kai@kaidalgleish.io"}

# new_list = make_sentiment_list(new_response)
# print new_list


if __name__ == '__main__':
    app.run(debug=True)
