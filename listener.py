from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import unirest
import json

ckey = ''
csecret = ''
atoken = ''
asecret = ''

def sentimentAnalysis(text):
    response = unirest.post("https://community-sentiment.p.mashape.com/text/",
                            headers={
                                "X-Mashape-Key": "",
                                "Content-Type": "application/x-www-form-urlencoded",
                                "Accept": "application/json"
                            },
                            params={
                                "txt": text
                            }
                            )

    return response.raw_body


class listener(StreamListener):
    count = 0
    averageSentiment = 0

    def on_data(self, data):

        tweet = data.split(',"text":"')[1].split('","source')[0]
        response = sentimentAnalysis(tweet)

        parsed_json = json.loads(response)
        confidence = parsed_json['result']['confidence']

        listener.averageSentiment += float(confidence)
        listener.count += 1
        sentiment = listener.averageSentiment / listener.count

        print response
        print sentiment
        print listener.count
        return True

    def on_error(self, status):
        print status


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Trump"])
