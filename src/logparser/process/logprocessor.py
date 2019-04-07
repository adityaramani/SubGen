import logging
import parser.logparser as logparser
from collections import defaultdict

logger = logging.getLogger("Processor")

def strip_meta(line):
	ind = line.find("]")
	if ind == -1:
		return None
	msg = line[ind+1:]
	return msg.strip()




class LogProcessor():
    def __init__(self,schema,callback):
        self.schema = schema
        self.keys = list(schema.keys())
        self.delimiters = [ schema[key]['delimiter'] for key in self.keys  ]
        self.parsers = {}
        self.last_seen_keys = defaultdict(str)
        self.cb =callback
    
    def get_parser(self, tid, key):

        if  tid  in self.parsers:
            if key in  self.parsers[tid]:
                return self.parsers[tid][key]
            else:
                self.parsers[tid][key] = logparser.LogParser(self.schema, key, self.cb)
                return self.parsers[tid][key]
        
        self.parsers[tid] = {}
        self.parsers[tid][key] = logparser.LogParser(self.schema, key, self.cb)
        return self.parsers[tid][key]
        


    def is_line_primary(self, line):
        for ind , delimiter in enumerate(self.delimiters):
            if delimiter in line:
                logger.debug("Checking Primary key in line : " + line)
                l = list(map(lambda x: x.strip(), line.split(delimiter)))
                key = l[0]
                val = l[1]
                if self.keys[ind]  == key:
                    return key , val
        
        return None,None
        
    def __get_TID__(self, line):
        index = line.find(']')
        if index  == -1:
            logger.info('Not a valid Log line' + line)
            return

        return line[:index].split(' ')[2]
        
    def read_line(self, line):
        
        tid = self.__get_TID__(line)
        
        if tid is not None:
            stripped_line = strip_meta(line)
            key, val = self.is_line_primary(stripped_line)
            if key is not None:
                logger.debug(key  + '   '   +val + '   ' + tid )

                parser = self.get_parser(tid, key)
                self.last_seen_keys[tid] = key
                return parser.insert(line,True)

            else:
                last_seen = self.last_seen_keys[tid]
                if last_seen == '':
                    return False
        
                parser = self.get_parser(tid,last_seen)
                return parser.insert(line)
        
        return False
            