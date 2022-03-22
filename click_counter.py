import requests

token = '0e4a5290fdc42bfdf00ab2609dca104e16c12a29'
token1 = '17c09e22ad155405159ca1977542fecf00231da7'
url  = 'https://api-ssl.bitly.com/v4/user'
web_url = 'google.com'
payload = {'Authorization': f'Bearer {token}',
                       
}
response = requests.get(url, headers=payload)
response.raise_for_status()
print(response.json())