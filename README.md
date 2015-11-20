![image](/static/welcome.png)

####*Slack-o-meter allows rapid visual analysis of traffic and mood across channels within a Slack team.*




### The Tech

* [Slack] - A messaging app for teams. Using OAuth, users can allow Slack-o-meter to access their account. With a series of API calls, Slack-o-meter gets the name of the authorized team, a list of the channels, and the recent history of each channel.

* [Sentiment140] - Public sentiment analysis optimized for Twitter, created by Stanford Graduate students. Given a series of comments via JSON, the Sentiment140 bulk classifier returns a sentiment rating from 0-4 for each, with 0 being very negative and 4 being very positive. 

* [D3] - Library with a huge variety of graphs and charts. Slack-o-meter uses a pack layout, a series of bubbles with color corresponding to sentiment and size to traffic over the last week. Data from Slack is processed into a Python dictionary, then passed into D3 using JSON. D3 generates svg elements with unique attributes for each item in the JSON. 




### Installation
In order to run Slack-o-meter on your computer, you'll need to make a Slack app which redirects to "/slacked", and generate a client key and secret. This can be done in a few minutes through [Slack's API portal.](https://api.slack.com/)

Clone repo:
```sh
$ git clone https://github.com/KaiDalgleish/slackometer.git slackometer
$ cd slackometer
```

Install dependencies:
```sh
$ pip install -r requirements.txt
```

Source secrets to your environment:
```sh
$ export CLIENT_ID=[Your client id here, for Slack]
$ export CLIENT_SECRET=[Your secret here, for Slack]
$ export MYEMAIL=[Your email here, for Sentiment140]
```

Run Slackometer server:
```sh
$ python server.py
```
View in your browser, probably at http://127.0.0.1:5000/ 




### Using Slack-o-meter

- Sign in to Slack using OAuth by clicking "Get Team"

![image](/static/allow_slack.png)

- Wait for the APIs to do their magic... then see a visual representation of your team! Color corresponds to average sentiment, while size corresponds to traffic. Hover to see the name of each channel.

![image](/static/bubbles.png)

