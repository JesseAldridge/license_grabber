import json, re

import requests

with open('packages.txt') as f:
  text = f.read()
lines = text.splitlines()
name_version = [re.split('==|<=|>=|<|>', line) for line in lines]

for t in name_version:
  try:
    name, version = t
  except ValueError:
    print 'could not process:', t
  json_str = requests.get('https://pypi.python.org/pypi/{}/json'.format(name)).content
  package_dict = json.loads(json_str)
  print name, package_dict['info']['license']
