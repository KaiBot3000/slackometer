# channel class 

class Channel(object):
    # will take in channel tuple

    def __init__(self, channel_tuple, user_token):
        self.name = channel_tuple[0]
        self.id = channel_tuple[1]
        self.ownertoken = user_token # this is a messy solution

        # these have been rewritten to be oo
        self.slack_history = get_channel_history()
        self.history_dict = make_history_dictionary()


    def get_channel_history(self):
        """Returns history of the channel"""

        history_params = {"token": self.ownertoken, 
                            "channel": self.id,
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


    def make_history_dictionary(self):
        """Converts a message list into a dictionary for sentiment analysis"""

        # dictionary = {"data":[
        #                     {"text": "I love Titanic."}, 
        #                     {"text": "I hate Titanic."}
        #                     ]}

        msg_dictionary = {}
        msg_text_list = []

        for msg in self.slack_history:
            msg_dict = {}
            msg = clean_msg(msg)
            msg_dict["text"] = msg
            msg_text_list.append(msg_dict)

        msg_dictionary["data"] = msg_text_list

        return msg_dictionary

# TODO: this should probably take the whole object's messages, not a single message (to be a class method)
    def clean_msg(self, msg):
        """Takes single message, removes user tags and links, returns stripped message"""

        # things to remove: <usernames> <links...>

        cleaned_msg = re.sub("[<].*?[>]", "", msg)

        return cleaned_msg


    def get_sentiment(self, msg_dictionary):
        """Given a message dictionary, makes an API call to Sentiment140 to get sentiments"""

        msg_dictionary["appid"] = MYEMAIL
        sentiment_data = json.dumps(msg_dictionary)

        sentiment_api_call = urlopen('http://www.sentiment140.com/api/bulkClassifyJson', sentiment_data)
        sentiment_response = sentiment_api_call.read()
         
        return sentiment_response

    def make_sentiment_list(self, sentiment_dict):
        """Given the sentiment response dictionary, makes list of just the sentiment values"""

        sentiment_list = []

        for sentiment in sentiment_dict["data"]:
            sentiment_list.append(sentiment["polarity"])

        return sentiment_list


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
