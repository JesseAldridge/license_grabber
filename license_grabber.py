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
  license_str = package_dict['info']['license']
  for safe_license in ('MIT', 'BSD', 'Apache', 'PSFL'):
    if re.search(r'\b{}\b'.format(safe_license), license_str):
      break
  else:
    print name, license_str
