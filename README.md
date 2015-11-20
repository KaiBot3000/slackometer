![image](/static/welcome.png)
#*Slack-o-meter allows rapid visual analysis of traffic and mood across channels within a Slack team.*



### The Tech

* [Slack] - A messaging app for teams. Using OAuth, users can allow Slack-o-meter to access their account. With a series of API calls, Slack-o-meter gets the name of the authorized team, a list of the channels, and the recent history of each channel.

* [Sentiment140] - Public sentiment analysis optimized for Twitter, created by Stanford Graduate students. Given a series of comments via JSON, the Sentiment140 bulk classifier returns a sentiment rating from 0-4 for each, with 0 being very negative and 4 being very positive. 

* [D3] - Library with a huge variety of graphs and charts. Slack-o-meter uses a pack layout, a series of bubbles with color corresponding to sentiment and size to traffic over the last week. Data from Slack is processed into a Python dictionary, then passed into D3 using JSON. D3 generates svg elements with unique attributes for each item in the JSON. 


### The Stack

* [Python] - Backend code that manipulates incoming data, controls access to the database, and serves data to the webpage through a framework.
* [Flask] - Lightweight web framework which also provides support for jinja templating and unittests
* [Javascript] - Frontend code which allows for dynamic webpages
* [jQuery] - A Javascript library that simplifies DOM manipulation, including creating event handlers for user interaction
* [HTML] - Displays information on the web
* [CSS] - Styles webpages

### Installation

Clone repo:
```sh
$ git clone https://github.com/KaiDalgleish/slackometer.git slackometer
$ cd slackometer
```

Install dependencies:
```sh
$ pip install -r requirements.txt
```

Run Slackometer server:
```sh
$ python server.py
```
View in your browser, probably at http://127.0.0.1:5000/ 

### Using Slack-o-meter

-Sign in to Slack using OAuth by clicking "Get Team"
![image](/static/allow_slack.png)

- See a visual representation of your team! Color corresponds to average sentiment, while size corresponds to traffic. 

![image](/static/bubbles.png)

