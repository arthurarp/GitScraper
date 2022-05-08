import sys
import requests
from bs4 import BeautifulSoup

class GitService:
    def __init__(self):
        self.BASE_URL = 'https://github.com/'
        self.suffix = '?tab=followers'

    def get_all_followers(self, username):
        followers_list = []
        result = requests.get(self.BASE_URL + username + self.suffix)
        html_doc = result.content
        soup = BeautifulSoup(html_doc, 'html.parser')
        followers_list_html = soup.find_all(
            "div", 
            {"class": "d-table table-fixed col-12 width-full py-4 border-bottom color-border-muted"}
        )
        for each_follower in followers_list_html:
            href = each_follower.find_all('a')[0].get('href')
            followers_list.append(href.strip('/'))
            # print(href, file=sys.stderr)
        return followers_list