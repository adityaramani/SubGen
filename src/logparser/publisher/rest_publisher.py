import requests
from urllib.parse import urljoin
import logging
import json

logger = logging.getLogger(__name__)


class RestPublisher():
    def __init__(self,sch, endpoint):
        #endpoint must be specified with trailing '/' eg http:/192.186.1.1/interface/write/
        self.schema = sch
        self.endpoint = endpoint

    
    def write_schema(self,key,file_name, version="0.1",description="Table Description"):
        url  = urljoin(self.endpoint, file_name)
        headers = [key] + self.schema[key]['fields']
        meta_data = self.schema[key]['field_mdt']
        data_types = [self.schema[key]['type']] + [ meta_data[field]['type'] for field in self.schema[key]['fields']   ] 
        column_desc = [self.schema[key]['desc']] + [ meta_data[field]['desc'] for field in self.schema[key]['fields']   ] 
        payload = [version, description, ",".join(headers), ",".join(data_types) , ",".join(column_desc),'']
        payload_encoded = '\n'.join(payload)
        request_body = {'line': payload_encoded}
        response = requests.post(url ,json=request_body )
        logger.info(response)
        logger.info("Posted Data to " + url  + json.dumps(request_body))
        
    def write_data(self,key,file_name,data):
        url  = urljoin(self.endpoint, file_name)
        fields = [key] + self.schema[key]['fields']
        payload = [ data[field]  for field in fields   ]
        payload_encoded = ','.join(payload) + '\n'
        request_body = {'line': payload_encoded}
        response = requests.put(url ,json=request_body)
        logger.debug('PUT Data to ' + url  + json.dumps(request_body))
        logger.debug(response)
        