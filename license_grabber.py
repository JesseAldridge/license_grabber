import json, re

import requests


def main():
  with open('packages.txt') as f:
    text = f.read()
  lines = text.splitlines()
  name_version = [re.split('==|<=|>=|<|>', line) for line in lines]

  for t in name_version:
    try:
      package_name, version = t
    except ValueError:
      print 'could not process:', t
    get(package_name)

def get(package_name, debug=False):
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
  for safe_license in ('MIT', 'BSD', 'Apache', 'PSFL'):
    if re.search(r'\b{}\b'.format(safe_license), license_str):
      break
  else:
    print package_name, license_str

if __name__ == '__main__':
  main()
  # get('zipstream', debug=True)
