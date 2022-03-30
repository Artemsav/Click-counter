import argparse
from urllib import response
from urllib.parse import urlparse

import requests
from environs import Env


def shorten_link(token, url, domain):
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'long_url':url, 'domain':domain}
    bitlinks_url  = 'https://api-ssl.bitly.com/v4/bitlinks'
    response = requests.post(bitlinks_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, link):
    parsed = urlparse(link)
    clean_link = f'{parsed.netloc}{parsed.path}'
    bitlinks_url  = f'https://api-ssl.bitly.com/v4/bitlinks/{clean_link}/clicks/summary'
    headers = {'Authorization': f'Bearer {token}'}
    params = {'unit': 'day', 'units': '-1'}
    response = requests.get(bitlinks_url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(token, url):
    parsed = urlparse(url)
    clean_link = f'{parsed.netloc}{parsed.path}'
    bitlinks_url  = f'https://api-ssl.bitly.com/v4/bitlinks/{clean_link}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(bitlinks_url, headers=headers)
    return response.ok


def parse_user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help= 'URL address of link to be shortened')
    args = parser.parse_args()
    return args


def validate_link(url):
    response = requests.get(url)
    return response.raise_for_status()


if __name__=='__main__':
    env = Env()
    env.read_env()
    token = env.str('BITLY_TOKEN')
    domain = env.str('DOMAIN', 'bit.ly')
    user_input = parse_user_input()
    url = user_input.url
    try:
        validate_link(url)
        if is_bitlink(token, url):
            try:
                total_clicks = count_clicks(token, url)
                print('Clicks', total_clicks)
            except requests.exceptions.HTTPError:
                print('Incorect link')
        else:
            link = shorten_link(token, url, domain)
            print('Битлинк', link)
    except requests.exceptions.ConnectionError as e:
        print(' Incorect link', '\n', f'Error: {e}')
