import sys
import requests
from bs4 import BeautifulSoup

class GitService:
    def __init__(self):
        self.BASE_URL = 'https://github.com/'

    def get_all_followers(self, username):
        suffix = '?tab=followers'
        followers_list = []
        result = requests.get(self.BASE_URL + username + suffix)
        html_doc = result.content
        soup = BeautifulSoup(html_doc, 'html.parser')
        followers_list_html = soup.find_all(
            "div", 
            {"class": "d-table table-fixed col-12 width-full py-4 border-bottom color-border-muted"}
        )
        for each_follower in followers_list_html:
            href = each_follower.find_all('a')[0].get('href')
            followers_list.append(href.strip('/'))
        return followers_list

    def get_all_following(self, username):
        suffix = '?tab=following'
        following_list = []
        result = requests.get(self.BASE_URL + username + suffix)
        html_doc = result.content
        soup = BeautifulSoup(html_doc, 'html.parser')
        following_list_html = soup.find_all(
            "div", 
            {"class": "d-table table-fixed col-12 width-full py-4 border-bottom color-border-muted"}
        )
        for each_following in following_list_html:
            href = each_following.find_all('a')[0].get('href')
            following_list.append(href.strip('/'))
        return following_list