# channel class 

class Channel(object):
    # will take in channel tuple


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
        #                     {"text": "I love Titanic."}, 
        #                     {"text": "I hate Titanic."}
        #                     ]}

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

        # things to remove: <usernames> <links...>

        cleaned_msg = re.sub("[<].*?[>]", "", msg)

        return cleaned_msg


    def get_sentiment(msg_dictionary):
        """Given a message dictionary, makes an API call to Sentiment140 to get sentiments"""

        msg_dictionary["appid"] = MYEMAIL
        sentiment_data = json.dumps(msg_dictionary)

        sentiment_api_call = urlopen('http://www.sentiment140.com/api/bulkClassifyJson', sentiment_data)
        sentiment_response = sentiment_api_call.read()
         
        return sentiment_response

    def make_sentiment_list(sentiment_dict):
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
