import sys
import json
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
    
    def get_user_info(self, username):
        prefix = 'https://avatars.githubusercontent.com/u/'
        result = requests.get(self.BASE_URL + username)
        html_doc = result.content
        soup = BeautifulSoup(html_doc, 'html.parser')
        name_span = soup.find('span', {"class": "p-name vcard-fullname d-block overflow-hidden"})
        name = name_span.text.strip()
        html_user_raw_data = soup.find_all(
            'a',
            {'class': 'UnderlineNav-item js-responsive-underlinenav-item selected'},
        )[0]
        raw_data = html_user_raw_data.get('data-hydro-click')
        info = json.loads(raw_data)
        user_id = str(info['payload']['profile_user_id'])
        data = {
            'username': username,
            'name': name,
            'image': prefix + user_id
        }
        return data