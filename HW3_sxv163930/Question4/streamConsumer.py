import os 
import nltk
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

sid = SentimentIntensityAnalyzer()

def write_to_file(tweet, sentiment):
	with open("q4.out", "a") as myfile:
		myfile.write(tweet + " - " + sentiment + "\n")

def calc_sentiment(ss):
	sent_to_sentiment = {
		"neg": "Negative",
		"pos": "Positive",
		"neu": "Neutral"
	}
	i = 0.0
	s = None
	for k in ss:
		if k != 'compound' and ss[k] > i:
			s = k
			i = ss[k]
	return sent_to_sentiment[s]

def create_out(fn):
	try:
		file = open(fn, 'r')
	except IOError:
		file = open(fn, 'w')

def analyze(tweet):
	ss = sid.polarity_scores(tweet)
	sentiment = calc_sentiment(ss)
	print(tweet)
	print(ss)
	create_out("q4.out")
	write_to_file(tweet, sentiment)
	return tweet

# Create a local StreamingContext with two working thread and batch interval of 1 second.
sc = SparkContext(appName="PythonSparkStreamingKafka")
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 60) # 1 - batchDuration 

# connect to kafka
kafkaStream = KafkaUtils.createStream(ssc, 'localhost:2181', 'spark-streaming', {'twitter': 1})

parsed = kafkaStream.count().map(lambda x:'Tweets in this batch: %s' % x).pprint()
tweets = kafkaStream.map(lambda v: analyze(v[1]))
tweets.pprint()
ssc.start()
ssc.awaitTermination()
