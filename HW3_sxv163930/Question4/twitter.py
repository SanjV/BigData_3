from kafka import KafkaProducer
from kafka.errors import KafkaError
from prettytable import PrettyTable
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os
import sys
import tempfile

# tweet connections
access_token = "204320576-wo3XqNFqgwTuvmiHU7lHeo22DHm7gxMC4HmJ1qWd"
access_token_secret = "2auVlMywAUMvHdOslrTBU4YOy4sfbB3Adcd7j9LpkPGXN"
consumer_key = "2iamBcyiJZKAkQVAdgBo8k1Pt"
consumer_secret = "egtX7usY1ve9RRf4XS2fHal87Hz9V0C7i72DHBsPPmq0LIdEXX"

# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_status(self, data):
        print(data._json)
        return True

    def on_error(self, status):
        print("Error: ", status)

    @staticmethod
    def read_request(logfile='../scrapy.log'):
        print("Allowable Operation List: ")
        t = PrettyTable(["Operator", "Find tweets"])
        t.add_row(['twitter search', 'containing both "twitter" and "search". This is the default operator.'])
        t.add_row(['"happy hour"', 'containing the exact phrase "happy hour".'])
        t.add_row(['love OR hate', 'containing either "love" or "hate" (or both).'])
        t.add_row(['beer **-**root', 'containing "beer" but not "root".'])
        t.add_row(['**#**haiku', 'containing the hashtag "haiku".'])
        t.add_row(['**from:**alexiskold', 'sent from person "alexiskold".'])
        t.add_row(['**to:**techcrunch', 'sent to person "techcrunch".'])
        t.add_row(['**@**mashable', 'referencing person "mashable".'])
        t.add_row(['"happy hour" near:"san francisco"', 'containing the exact phrase "happy hour" and sent near "san francisco".'])
        t.add_row(['**near:**NYC **within:**15mi', 'sent within 15 miles of "NYC".'])
        t.add_row(['superhero **since:**2010-12-27', 'containing "superhero" and sent since date "2010-12-27" (year-month-day).'])
        t.add_row(['ftw **until:**2010-12-27', 'containing "ftw" and sent up to date "2010-12-27".'])
        t.add_row(['movie -scary :)', 'containing "movie", but not "scary", and with a positive attitude.'])
        t.add_row(['flight :(', 'containing "flight" and with a negative attitude.'])
        t.add_row(['traffic ?', 'containing "traffic" and asking a question.'])
        t.add_row(['hilarious filter:links', 'containing "hilarious" and linking to URLs.'])
        t.add_row(['news source:twitterfeed', 'containing "news" and entered via TwitterFeed'])
        print(t)
        request = input("Please enter your request, separate different operations by comma ,: ")
        return request 

    @staticmethod
    def start_crawl():
        # This handles Twitter authetification and the connection to Twitter Streaming API
        l = StdOutListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth=auth, listener=l)
        request = l.read_request()
        print("Executing requests: %s" % (request,))
        # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
        with open('tempbuffer.txt', 'w') as f:
            with open("tmpfile_path.txt", "w") as f2:
                f2.write(f.name)
            sys.stdout = f
            stream.filter(track=[request])


StdOutListener.start_crawl()
# start_crawl()

# while True:
# 	for i in range(100):
# 		producer.send('test', ("tt1e"+str(i)).encode('utf-8'))
# 	producer.flush()

