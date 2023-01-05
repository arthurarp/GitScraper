import sys
import json
import requests
from bs4 import BeautifulSoup
from functions.graph import Graph

class GitService:
    def __init__(self):
        self.BASE_URL = 'https://github.com/'
        self.teste = 123

    def get_all_followers(self, username):
        suffix = '?tab=followers'
        followers_list = []
        result = requests.get(self.BASE_URL + username + suffix)
        print(username, ' ', result.status_code, file=sys.stderr)
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
        print(username, ' ', result.status_code, file=sys.stderr)
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
        print(username, ' ', result.status_code, file=sys.stderr)
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

    def search_by_levels(self, graph, users_to_visit_queue, level):
        while len(users_to_visit_queue) > 0:
            current_user = users_to_visit_queue.pop()
            all_followers = self.get_all_followers(current_user)
            for follower in all_followers:
                if not graph.vertex_exists(follower):
                    user_info = self.get_user_info(follower)
                    graph.add_vertex(
                        user_info['username'], 
                        user_info['name'], 
                        user_info['image'], 
                    )
                graph.add_edge(follower, current_user)

            all_following = self.get_all_following(current_user)
            for following in all_following:
                if not graph.vertex_exists(following):
                    user_info = self.get_user_info(following)
                    graph.add_vertex(
                        user_info['username'], 
                        user_info['name'], 
                        user_info['image'], 
                    )
                graph.add_edge(current_user, following)
        
            if level > 1:
                users_to_visit_queue += all_followers + all_following
                level -= 1

        return graph.get_plot_data()
    
    def get_graph(self, username, level):
        user_info = self.get_user_info(username)
        print('teste', file=sys.stderr)
        graph = Graph(user_info)
        if level == 0:
            return graph.get_plot_data()

        return self.search_by_levels(graph, [username], level)

