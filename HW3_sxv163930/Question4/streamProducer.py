from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json
import pyinotify
import re
import asyncore
from kafka import KafkaProducer
from kafka.errors import KafkaError
import time
from ast import literal_eval


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, process_model):
        self.filter = process_model

    # evt has useful properties, including pathname
    def process_IN_MODIFY(self, event):
        self.filter.process()

class ReadStream(object):
	def __init__(self, producer):
		super(ReadStream, self).__init__()
		path = "tmpfile_path.txt"
		with open(path, 'r') as f:
		    path = f.readline()
		self.input_path = path
		self.lineNum = 0
		self.byteoffset = 0
		self.pattern = re.compile(r'[.-@#\w]+')
		self.url_pattern = re.compile(r'(http[s]://[\w./]+)*')
		self.remove_tag_pattern = re.compile(r'(#\w)+')
		self.isdigit = re.compile(r'\d+|\d+.jpg')
		self.producer = producer

	def process_line(self, line):
		print("Entered process_line")
		time = line.get('created_at', None)
		content = line.get('text', None)
		place = line.get('user', {}).get('place', None)
		source = line.get('source', None)
		nline = '#'*50+"\n"
		nline += "Time: %s | Place: %s | Source: %s" % (time, place, source)
		nline += "\n"
		nline += content
		nline += '\n'+'#'*50+"\n\n"
		
		data = ""
		# if time:
		# 	data += time
		# else:
		# 	data += ""
		# data += "::"
		if content:
			data += content
		else:
			data += ""
		# data += "::"
		# if place:
		# 	data += place
		# else:
		# 	data += ""
		# data += "::"
		# if source:
		# 	data += source 
		# else:
		# 	data += ""

		return nline, data

	def process(self):
		lineNum = 0
		with open(self.input_path, "r") as f:
			f.seek(self.byteoffset)
			for line in f:
				line = line.strip()
				if not line:
					print("Entered if")
					continue
				try:
					# re.compile("(?P<key>\w+)=(?P<value>\w+)")
					# expre = re.compile("(?P<key>\w+)=(?P<value>\w+)")
					# pairs = dict(re.findall(expre, line))
					line = line.replace("u'", "'", len(line))
					# print(line)
					# m = json.dumps(line)
					# n = json.loads(m)
					line = literal_eval(line)
					# print(pairs)
					# print(n)
					# print(type(line))
				except ValueError:
					print("Exception raised")
					time.sleep(5)
					return
				line, data = self.process_line(line)
				self.producer.send("twitter", data.encode('utf-8'))
				time.sleep(1)
			self.byteoffset = f.tell()

	def start(self):
	    # The watch manager stores the watches and provides operations on watches
	    wm = pyinotify.WatchManager()
	    mask = pyinotify.IN_MODIFY  # watched events
	    handler = EventHandler(self)
	    notifier = pyinotify.AsyncNotifier(wm, handler)
	    wdd = wm.add_watch(self.input_path, mask)
	    asyncore.loop()

# Kafka
# create a producer for json message
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# stream reader 
reader = ReadStream(producer)
reader.start()

