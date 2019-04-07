import logging
import json
logger = logging.getLogger("Parser")

def strip_meta(line):
	ind = line.find("@")
	if ind == -1:
		return None
	msg = line[ind+1:]
	return msg.strip()



class LogParser():

	def __init__(self, schema, key,cb_flush):
		self.__schema__ = schema[key]
		self.delimiter = self.__schema__['delimiter']
		self.__data_store__ = {}
		self.keys = self.__schema__['fields']
		self.__flush__ = cb_flush
		self.pk = key
		self.csv_path  = schema[key]['csv_path']

	def insert(self, line, primary_key=False):
		line  = strip_meta(line)
		if self.delimiter in line:
			l = list(map(lambda x: x.strip(), line.split(self.delimiter)))
			key = l[0]
			value = l[1]
			if primary_key:
				self.reset_store()
				self.__store__(key, value)
				return True

			elif key in self.keys:	
				self.__store__(key, value)
				
				if len(self.__data_store__.keys()) == len(self.keys) + 1 :
					self.flush()
					self.reset_store()
			
				return True
		
		return False

	
	def __store__(self,key, value):
		self.__data_store__[key] = value
	
	def reset_store(self):
		self.__data_store__ = dict({})

	def flush(self):
		return self.__flush__( json.dumps(self.__data_store__)+',\n')

