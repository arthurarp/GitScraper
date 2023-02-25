import sys
import json
import requests
from bs4 import BeautifulSoup
from functions.graph import Graph
from dotenv import dotenv_values

class GitService:
    def __init__(self):
        self.BASE_URL = 'https://github.com/'
        self.token = dotenv_values(".env")['GIT_TOKEN']

    def get_all_followers(self, username):
        suffix = '?tab=followers'
        followers_list = []
        result = requests.get(self.BASE_URL + username + suffix)
        # print(username, ' ', result.status_code, file=sys.stderr)
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

    def get_all_following(self, username, graph):
        url = 'https://api.github.com/users/{}/following'.format(username)
        result = requests.get(url, headers={'Authorization': 'Bearer ' + self.token}).json()
        
        following_list = [each_user['login'] for each_user in result]
        for following in result:
            if not graph.vertex_exists(following['login']):
                graph.add_vertex(
                        following['login'], 
                        following['login'], 
                        following['avatar_url'], 
                    )
            graph.add_edge(username, following['login'])
        return following_list
    

    def search_by_levels(self, graph, users_to_visit_queue, level):
        while len(users_to_visit_queue) > 0:
            current_user = users_to_visit_queue.pop()
            # all_followers = self.get_all_followers(current_user)
            # for follower in all_followers:
            #     if not graph.vertex_exists(follower):
            #         user_info = self.get_user_info(follower)
            #         if not user_info:
            #             continue
            #         graph.add_vertex(
            #             user_info['username'], 
            #             user_info['name'], 
            #             user_info['image'], 
            #         )
            #     graph.add_edge(follower, current_user)

            all_following = self.get_all_following(current_user, graph)#[:15]#[::-1][:15]
        
            if level > 1: # corrigir (lógica errada)
                # users_to_visit_queue += all_followers 
                users_to_visit_queue += all_following
                level -= 1

        return graph.get_plot_data()

    def get_user_info(self, username):
        url = 'https://api.github.com/users/{}'.format(username)
        try:
            result = requests.get(url, headers={'Authorization': 'Bearer ' + self.token}).json()
            print(result, file=sys.stderr)
            return {
                'username': result['login'],
                'name':  result['name'],
                'image':  result['avatar_url']
            }
        except Exception as err:
            print(err, file=sys.stderr)
            return None

    def get_graph(self, username, level):
        user_info = self.get_user_info(username)
        if not user_info:
            return None
        graph = Graph(user_info)
        if level == 0:
            return graph.get_plot_data()

        return self.search_by_levels(graph, [username], level)

