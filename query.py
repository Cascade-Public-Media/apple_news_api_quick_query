import base64
import ConfigParser
import hmac
import json
import requests

from hashlib import sha256
from datetime import datetime

config = ConfigParser.ConfigParser()
config.read('config.ini')

channel_id = config.get('config', 'channel_id')
api_key_id = config.get('config', 'api_key_id')
api_key_secret = config.get('config', 'api_key_secret')

url = 'https://news-api.apple.com/channels/%s' % channel_id

path = raw_input('Enter path: ')

url += path

date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

canonical_request = 'GET' + url + str(date)

key = base64.b64decode(api_key_secret)

hashed = hmac.new(key, canonical_request, sha256)
signature = hashed.digest().encode("base64").rstrip('\n')

authorization = 'HHMAC; key=%s; signature=%s; date=%s' % (api_key_id, str(signature), date)

headers = {'Authorization': authorization}
response = requests.get(url, headers=headers)

data = json.loads(response.text)
print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
