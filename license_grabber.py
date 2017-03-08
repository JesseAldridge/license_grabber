import json, re

import requests

def weird_licenses():
  for line, license_str in each_license():
    for safe_license in ('MIT', 'BSD', 'Apache', 'PSFL'):
      if re.search(r'\b{}\b'.format(safe_license), license_str):
        break
    else:
      print line, license_str

def each_license():
  with open('packages.txt') as f:
    text = f.read()

  for line in text.splitlines():
    name_version = re.split('==|<=|>=|<|>', line)
    try:
      package_name, version = name_version
    except ValueError:
      print 'could not process:', line
      continue
    yield line, pull_license(package_name)

def pull_license(package_name, debug=False):
  json_str = requests.get('https://pypi.python.org/pypi/{}/json'.format(package_name)).content
  package_dict = json.loads(json_str)
  if debug:
    print json.dumps(package_dict, indent=2)
  license_str = package_dict['info']['license']
  if license_str == 'UNKNOWN':
    for classifier in package_dict['info']['classifiers']:
      if classifier.startswith('License'):
        license_str = classifier
        break
  return license_str

if __name__ == '__main__':
  for line, license_str in each_license():
    print line, license_str
  # pull_license('zipstream', debug=True)
