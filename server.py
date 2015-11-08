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
        # print response
        user_token = response["access_token"]




        # get list of channels for user
        channel_list = get_channel_list(user_token)

        # # for channel in channel_list:
        # #     print channel
            
        # # get history for one channel
        # first_channel = channel_list[0]
        # first_channel_history = get_channel_history(user_token, first_channel)
        # print first_channel_history
        
        # # convert history into python dictionary
        # msg_dictionary = make_history_dictionary(first_channel_history)

        # # use API call to get sentiment analysis
        # sentiment = get_sentiment(msg_dictionary)

        # print sentiment

        # sentiment_list = make_sentiment_list(sentiment)
        # print sentiment_list

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

            print sentiment_tuple, channel[0]

    # should probably redirect to route that builds channel objects, pass user token
    # return redirect("/bubblebuilder.json", user_token=user_token)

    return "authorized"


# @app.route("/bubblebuilder.json")
# def build_bubbles():
#     """Gets channel history and builds bubble json"""

    # user_token = get the id from the post request

    # get channel list, using user token

    # for channel, 
        # build objects
        # get channel history
        # add to objects




    # return json for d3 


@app.route("/bubble")
def bubble():
    """Test route for building d3 bubble chart"""

    return render_template("cats.html")


@app.route("/cats.json")
def send_cats():
    """Test route for building d3 bubble chart"""

    cats = {"name": "cats",
            "children": [
            {"name": "Guido", "size": 160},
            {"name": "Darwin", "size": 110},
            {"name": "Mika", "size": 100},
            {"name": "Kitin", "size": 150},
            {"name": "Pirate Jack", "size": 180}
            ]}

    return jsonify(cats)


@app.route("/flare")
def flare():
    """Test route for building d3 bubble chart"""

    return render_template("bubble.html")   


@app.route("/flare.json")
def send_flare():
    """Test route for building d3 bubble chart"""

    flare = {"name": "flare",
             "children": [
              {
               "name": "analytics",
               "children": [
                {
                 "name": "cluster",
                 "children": [
                  {"name": "AgglomerativeCluster", "size": 3938},
                  {"name": "CommunityStructure", "size": 3812},
                  {"name": "HierarchicalCluster", "size": 6714},
                  {"name": "MergeEdge", "size": 743}
                 ]
                },
                {
                 "name": "graph",
                 "children": [
                  {"name": "BetweennessCentrality", "size": 3534},
                  {"name": "LinkDistance", "size": 5731},
                  {"name": "MaxFlowMinCut", "size": 7840},
                  {"name": "ShortestPaths", "size": 5914},
                  {"name": "SpanningTree", "size": 3416}
                 ]
                },
                {
                 "name": "optimization",
                 "children": [
                  {"name": "AspectRatioBanker", "size": 7074}
                 ]
                }
               ]
              },
              {
               "name": "animate",
               "children": [
                {"name": "Easing", "size": 17010},
                {"name": "FunctionSequence", "size": 5842},
                {
                 "name": "interpolate",
                 "children": [
                  {"name": "ArrayInterpolator", "size": 1983},
                  {"name": "ColorInterpolator", "size": 2047},
                  {"name": "DateInterpolator", "size": 1375},
                  {"name": "Interpolator", "size": 8746},
                  {"name": "MatrixInterpolator", "size": 2202},
                  {"name": "NumberInterpolator", "size": 1382},
                  {"name": "ObjectInterpolator", "size": 1629},
                  {"name": "PointInterpolator", "size": 1675},
                  {"name": "RectangleInterpolator", "size": 2042}
                 ]
                },
                {"name": "ISchedulable", "size": 1041},
                {"name": "Parallel", "size": 5176},
                {"name": "Pause", "size": 449},
                {"name": "Scheduler", "size": 5593},
                {"name": "Sequence", "size": 5534},
                {"name": "Transition", "size": 9201},
                {"name": "Transitioner", "size": 19975},
                {"name": "TransitionEvent", "size": 1116},
                {"name": "Tween", "size": 6006}
               ]
              },
              {
               "name": "data",
               "children": [
                {
                 "name": "converters",
                 "children": [
                  {"name": "Converters", "size": 721},
                  {"name": "DelimitedTextConverter", "size": 4294},
                  {"name": "GraphMLConverter", "size": 9800},
                  {"name": "IDataConverter", "size": 1314},
                  {"name": "JSONConverter", "size": 2220}
                 ]
                },
                {"name": "DataField", "size": 1759},
                {"name": "DataSchema", "size": 2165},
                {"name": "DataSet", "size": 586},
                {"name": "DataSource", "size": 3331},
                {"name": "DataTable", "size": 772},
                {"name": "DataUtil", "size": 3322}
               ]
              },
              {
               "name": "display",
               "children": [
                {"name": "DirtySprite", "size": 8833},
                {"name": "LineSprite", "size": 1732},
                {"name": "RectSprite", "size": 3623},
                {"name": "TextSprite", "size": 10066}
               ]
              },
              {
               "name": "flex",
               "children": [
                {"name": "FlareVis", "size": 4116}
               ]
              },
              {
               "name": "physics",
               "children": [
                {"name": "DragForce", "size": 1082},
                {"name": "GravityForce", "size": 1336},
                {"name": "IForce", "size": 319},
                {"name": "NBodyForce", "size": 10498},
                {"name": "Particle", "size": 2822},
                {"name": "Simulation", "size": 9983},
                {"name": "Spring", "size": 2213},
                {"name": "SpringForce", "size": 1681}
               ]
              },
              {
               "name": "query",
               "children": [
                {"name": "AggregateExpression", "size": 1616},
                {"name": "And", "size": 1027},
                {"name": "Arithmetic", "size": 3891},
                {"name": "Average", "size": 891},
                {"name": "BinaryExpression", "size": 2893},
                {"name": "Comparison", "size": 5103},
                {"name": "CompositeExpression", "size": 3677},
                {"name": "Count", "size": 781},
                {"name": "DateUtil", "size": 4141},
                {"name": "Distinct", "size": 933},
                {"name": "Expression", "size": 5130},
                {"name": "ExpressionIterator", "size": 3617},
                {"name": "Fn", "size": 3240},
                {"name": "If", "size": 2732},
                {"name": "IsA", "size": 2039},
                {"name": "Literal", "size": 1214},
                {"name": "Match", "size": 3748},
                {"name": "Maximum", "size": 843},
                {
                 "name": "methods",
                 "children": [
                  {"name": "add", "size": 593},
                  {"name": "and", "size": 330},
                  {"name": "average", "size": 287},
                  {"name": "count", "size": 277},
                  {"name": "distinct", "size": 292},
                  {"name": "div", "size": 595},
                  {"name": "eq", "size": 594},
                  {"name": "fn", "size": 460},
                  {"name": "gt", "size": 603},
                  {"name": "gte", "size": 625},
                  {"name": "iff", "size": 748},
                  {"name": "isa", "size": 461},
                  {"name": "lt", "size": 597},
                  {"name": "lte", "size": 619},
                  {"name": "max", "size": 283},
                  {"name": "min", "size": 283},
                  {"name": "mod", "size": 591},
                  {"name": "mul", "size": 603},
                  {"name": "neq", "size": 599},
                  {"name": "not", "size": 386},
                  {"name": "or", "size": 323},
                  {"name": "orderby", "size": 307},
                  {"name": "range", "size": 772},
                  {"name": "select", "size": 296},
                  {"name": "stddev", "size": 363},
                  {"name": "sub", "size": 600},
                  {"name": "sum", "size": 280},
                  {"name": "update", "size": 307},
                  {"name": "variance", "size": 335},
                  {"name": "where", "size": 299},
                  {"name": "xor", "size": 354},
                  {"name": "_", "size": 264}
                 ]
                },
                {"name": "Minimum", "size": 843},
                {"name": "Not", "size": 1554},
                {"name": "Or", "size": 970},
                {"name": "Query", "size": 13896},
                {"name": "Range", "size": 1594},
                {"name": "StringUtil", "size": 4130},
                {"name": "Sum", "size": 791},
                {"name": "Variable", "size": 1124},
                {"name": "Variance", "size": 1876},
                {"name": "Xor", "size": 1101}
               ]
              },
              {
               "name": "scale",
               "children": [
                {"name": "IScaleMap", "size": 2105},
                {"name": "LinearScale", "size": 1316},
                {"name": "LogScale", "size": 3151},
                {"name": "OrdinalScale", "size": 3770},
                {"name": "QuantileScale", "size": 2435},
                {"name": "QuantitativeScale", "size": 4839},
                {"name": "RootScale", "size": 1756},
                {"name": "Scale", "size": 4268},
                {"name": "ScaleType", "size": 1821},
                {"name": "TimeScale", "size": 5833}
               ]
              },
              {
               "name": "util",
               "children": [
                {"name": "Arrays", "size": 8258},
                {"name": "Colors", "size": 10001},
                {"name": "Dates", "size": 8217},
                {"name": "Displays", "size": 12555},
                {"name": "Filter", "size": 2324},
                {"name": "Geometry", "size": 10993},
                {
                 "name": "heap",
                 "children": [
                  {"name": "FibonacciHeap", "size": 9354},
                  {"name": "HeapNode", "size": 1233}
                 ]
                },
                {"name": "IEvaluable", "size": 335},
                {"name": "IPredicate", "size": 383},
                {"name": "IValueProxy", "size": 874},
                {
                 "name": "math",
                 "children": [
                  {"name": "DenseMatrix", "size": 3165},
                  {"name": "IMatrix", "size": 2815},
                  {"name": "SparseMatrix", "size": 3366}
                 ]
                },
                {"name": "Maths", "size": 17705},
                {"name": "Orientation", "size": 1486},
                {
                 "name": "palette",
                 "children": [
                  {"name": "ColorPalette", "size": 6367},
                  {"name": "Palette", "size": 1229},
                  {"name": "ShapePalette", "size": 2059},
                  {"name": "SizePalette", "size": 2291}
                 ]
                },
                {"name": "Property", "size": 5559},
                {"name": "Shapes", "size": 19118},
                {"name": "Sort", "size": 6887},
                {"name": "Stats", "size": 6557},
                {"name": "Strings", "size": 22026}
               ]
              },
              {
               "name": "vis",
               "children": [
                {
                 "name": "axis",
                 "children": [
                  {"name": "Axes", "size": 1302},
                  {"name": "Axis", "size": 24593},
                  {"name": "AxisGridLine", "size": 652},
                  {"name": "AxisLabel", "size": 636},
                  {"name": "CartesianAxes", "size": 6703}
                 ]
                },
                {
                 "name": "controls",
                 "children": [
                  {"name": "AnchorControl", "size": 2138},
                  {"name": "ClickControl", "size": 3824},
                  {"name": "Control", "size": 1353},
                  {"name": "ControlList", "size": 4665},
                  {"name": "DragControl", "size": 2649},
                  {"name": "ExpandControl", "size": 2832},
                  {"name": "HoverControl", "size": 4896},
                  {"name": "IControl", "size": 763},
                  {"name": "PanZoomControl", "size": 5222},
                  {"name": "SelectionControl", "size": 7862},
                  {"name": "TooltipControl", "size": 8435}
                 ]
                },
                {
                 "name": "data",
                 "children": [
                  {"name": "Data", "size": 20544},
                  {"name": "DataList", "size": 19788},
                  {"name": "DataSprite", "size": 10349},
                  {"name": "EdgeSprite", "size": 3301},
                  {"name": "NodeSprite", "size": 19382},
                  {
                   "name": "render",
                   "children": [
                    {"name": "ArrowType", "size": 698},
                    {"name": "EdgeRenderer", "size": 5569},
                    {"name": "IRenderer", "size": 353},
                    {"name": "ShapeRenderer", "size": 2247}
                   ]
                  },
                  {"name": "ScaleBinding", "size": 11275},
                  {"name": "Tree", "size": 7147},
                  {"name": "TreeBuilder", "size": 9930}
                 ]
                },
                {
                 "name": "events",
                 "children": [
                  {"name": "DataEvent", "size": 2313},
                  {"name": "SelectionEvent", "size": 1880},
                  {"name": "TooltipEvent", "size": 1701},
                  {"name": "VisualizationEvent", "size": 1117}
                 ]
                },
                {
                 "name": "legend",
                 "children": [
                  {"name": "Legend", "size": 20859},
                  {"name": "LegendItem", "size": 4614},
                  {"name": "LegendRange", "size": 10530}
                 ]
                },
                {
                 "name": "operator",
                 "children": [
                  {
                   "name": "distortion",
                   "children": [
                    {"name": "BifocalDistortion", "size": 4461},
                    {"name": "Distortion", "size": 6314},
                    {"name": "FisheyeDistortion", "size": 3444}
                   ]
                  },
                  {
                   "name": "encoder",
                   "children": [
                    {"name": "ColorEncoder", "size": 3179},
                    {"name": "Encoder", "size": 4060},
                    {"name": "PropertyEncoder", "size": 4138},
                    {"name": "ShapeEncoder", "size": 1690},
                    {"name": "SizeEncoder", "size": 1830}
                   ]
                  },
                  {
                   "name": "filter",
                   "children": [
                    {"name": "FisheyeTreeFilter", "size": 5219},
                    {"name": "GraphDistanceFilter", "size": 3165},
                    {"name": "VisibilityFilter", "size": 3509}
                   ]
                  },
                  {"name": "IOperator", "size": 1286},
                  {
                   "name": "label",
                   "children": [
                    {"name": "Labeler", "size": 9956},
                    {"name": "RadialLabeler", "size": 3899},
                    {"name": "StackedAreaLabeler", "size": 3202}
                   ]
                  },
                  {
                   "name": "layout",
                   "children": [
                    {"name": "AxisLayout", "size": 6725},
                    {"name": "BundledEdgeRouter", "size": 3727},
                    {"name": "CircleLayout", "size": 9317},
                    {"name": "CirclePackingLayout", "size": 12003},
                    {"name": "DendrogramLayout", "size": 4853},
                    {"name": "ForceDirectedLayout", "size": 8411},
                    {"name": "IcicleTreeLayout", "size": 4864},
                    {"name": "IndentedTreeLayout", "size": 3174},
                    {"name": "Layout", "size": 7881},
                    {"name": "NodeLinkTreeLayout", "size": 12870},
                    {"name": "PieLayout", "size": 2728},
                    {"name": "RadialTreeLayout", "size": 12348},
                    {"name": "RandomLayout", "size": 870},
                    {"name": "StackedAreaLayout", "size": 9121},
                    {"name": "TreeMapLayout", "size": 9191}
                   ]
                  },
                  {"name": "Operator", "size": 2490},
                  {"name": "OperatorList", "size": 5248},
                  {"name": "OperatorSequence", "size": 4190},
                  {"name": "OperatorSwitch", "size": 2581},
                  {"name": "SortOperator", "size": 2023}
                 ]
                },
                {"name": "Visualization", "size": 16540}
               ]
              }
             ]
            }

    return jsonify(flare)



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

# colors = RdYlGn: {
# 3: ["#fc8d59","#ffffbf","#91cf60"],
# 4: ["#d7191c","#fdae61","#a6d96a","#1a9641"],
# 5: ["#d7191c","#fdae61","#ffffbf","#a6d96a","#1a9641"],
# 6: ["#d73027","#fc8d59","#fee08b","#d9ef8b","#91cf60","#1a9850"],
# 7: ["#d73027","#fc8d59","#fee08b","#ffffbf","#d9ef8b","#91cf60","#1a9850"],
# 8: ["#d73027","#f46d43","#fdae61","#fee08b","#d9ef8b","#a6d96a","#66bd63","#1a9850"],
# 9: ["#d73027","#f46d43","#fdae61","#fee08b","#ffffbf","#d9ef8b","#a6d96a","#66bd63","#1a9850"],
# 10: ["#a50026","#d73027","#f46d43","#fdae61","#fee08b","#d9ef8b","#a6d96a","#66bd63","#1a9850","#006837"],
# 11: ["#a50026","#d73027","#f46d43","#fdae61","#fee08b","#ffffbf","#d9ef8b","#a6d96a","#66bd63","#1a9850","#006837"]
# }

if __name__ == '__main__':
    app.run(debug=True)
