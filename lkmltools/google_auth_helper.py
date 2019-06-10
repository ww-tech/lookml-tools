'''
    Authors:
        Carl Anderson (carl.anderson@weightwatchers.com)

'''
import os 
import json 
import base64 

class GoogleAuthHelper():

    def encode_service_account(self, raw_json):
        '''encode JSON to base64 representation

        Args:
            raw_json (JSON): raw Google service account JSON

        Returns:
            Base64 encoded Google service account JSON

        '''
        return base64.b64encode(json.dumps(raw_json).replace('\"', "\'").encode('utf-8'))

    def decode_service_account(self, encoded_json): 
        '''decode base64 representation back to JSON

        Args:
            encoded_json (bytes): output of encode_service_account, ie base64 encoded service account 

        Returns:
            service account JSON

        '''
        return json.loads(base64.b64decode(encoded_json).decode('utf8').replace('\'', '\"')) 

    def write_decoded_sa_json_to_file(self, encoded_json, filename='key.json'): 
        '''write decoded service account JSON to file

        Args:
            encoded_json (bytes): base64 encoded service account JSON
            filename (str): filename to write to

        Returns:
            nothing. Dumps service account to file

        '''
        with open(filename, 'w') as f: 
            json.dump(self.decode_service_account(encoded_json), f)
