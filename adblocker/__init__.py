import requests
import os

DEBUG = 'DEBUG' in os.environ and os.environ['DEBUG'] == '1'
HOSTS_FILE = '/etc/hosts'
FILTER_URLS = [
    'http://sbc.io/hosts/alternates/fakenews-gambling-porn-social/hosts'
]


def fetch_adblock_list():
    hosts_str = '\n'
    for url in FILTER_URLS:
        r = requests.get(url)
        hosts_str += r.text + '\n'
    return hosts_str
