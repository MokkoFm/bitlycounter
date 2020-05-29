from dotenv import load_dotenv
load_dotenv()
import argparse
import requests
import os
import json

def shorten_link(token, url, user_input):
    headers = {"Authorization": token}
    payload = {"long_url": user_input}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink

def count_clicks(token, url_for_count):
    headers = {"Authorization": token}
    payload = {"unit": "month"}
    response = requests.get(url_for_count, params=payload, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count

def main():
    token = os.getenv("APIKEY")
    parser = argparse.ArgumentParser(description='You can make a short link and count clicks')
    parser.add_argument('-l', '--link', help='Your link')
    your_link = parser.parse_args()

    if your_link.link:
      user_input = your_link.link
    else:
      user_input = input('Введите ссылку:')

    url = "https://api-ssl.bitly.com/v4/bitlinks"
    url_for_count = "https://api-ssl.bitly.com/v4/bitlinks/{0}/clicks/summary".format(user_input)
    checker = user_input.startswith("bit")

    if checker:
      try:
        clicks_count = count_clicks(token, url_for_count)
      except requests.exceptions.HTTPError as error:
        exit("Error with your link!\n{0}".format(error))
      print('Кликов было:', count_clicks(token, url_for_count))
    elif not checker:
      try:
        bitlink = shorten_link(token, url, user_input)
      except requests.exceptions.HTTPError as error:
        exit("Error with your link!\n{0}".format(error))
      print('Битлинк', shorten_link(token, url, user_input))
  

if __name__ == '__main__':
    main()
