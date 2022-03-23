import requests
import argparse
from urllib.parse import urlparse
from environs import Env


def shorten_link(token, url):
    api_token = {'Authorization': f'Bearer {token}'}
    payload = {'long_url': url}
    bitlinks_url  = 'https://api-ssl.bitly.com/v4/bitlinks'
    response = requests.post(bitlinks_url, json=payload, headers=api_token)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, link):
    parsed = urlparse(link)
    clean_link = f'{parsed.netloc}{parsed.path}'
    bitlinks_url  = f'https://api-ssl.bitly.com/v4/bitlinks/{clean_link}/clicks/summary'
    api_token = {'Authorization': f'Bearer {token}'}
    payload = {'unit': 'day', 'units': '-1'}
    response = requests.get(bitlinks_url, params=payload, headers=api_token)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(url):
    parsed = urlparse(url)
    clean_link = f'{parsed.netloc}{parsed.path}'
    bitlinks_url  = f'https://api-ssl.bitly.com/v4/bitlinks/{clean_link}'
    api_token = {'Authorization': f'Bearer {token}'}
    response = requests.get(bitlinks_url, headers=api_token)
    return response.ok


def parse_user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help= 'URL address of link to be shortened')
    args = parser.parse_args()
    return args


if __name__=='__main__':
    env = Env()
    env.read_env()
    token = env.str('TOKEN')
    user_input = parse_user_input()
    url = user_input.url
    if is_bitlink(url):
        try:
            total_clicks = count_clicks(token, url)
            print('Clicks', total_clicks)
        except requests.exceptions.HTTPError:
            print('Incorect link')
    else:
        try:
            link = shorten_link(token, url)
            print('Битлинк', link)
        except requests.exceptions.HTTPError:
            print('Incorect link')        
