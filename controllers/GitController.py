import sys
import json
from flask import jsonify, request
from services.GitService import GitService

class GitController:
    def __init__(self, app):
        self.app = app
        self.gitService = GitService()
        self.routes()

    def routes(self):
        @self.app.route('/<username>/followers', methods=['GET'])
        def get_followers(username):
          try:
            all_followers = self.gitService.get_all_followers(username)
            return jsonify(all_followers), 200
          except Exception as err:
            print(err, file=sys.stderr)
            return jsonify({'message': 'Error on getting user followers'}), 500

        @self.app.route('/<username>/following', methods=['GET'])
        def get_following(username):
          try:
            all_following = self.gitService.get_all_following(username)
            return jsonify(all_following), 200
          except Exception as err:
            print(err, file=sys.stderr)
            return jsonify({'message': 'Error on getting user following'}), 500
        
        @self.app.route('/<username>', methods=['GET'])
        def get_info(username):
          try:
            user_info = self.gitService.get_user_info(username)
            return jsonify(user_info), 200
          except Exception as err:
            print(err, file=sys.stderr)
            return jsonify({'message': 'Error on getting user info'}), 500

        # @self.app.route('/<username>/graph/<level>', methods=['GET'])
        # def get_graph(username, level):
        #   try:
        #     graph = self.gitService.get_graph(username, int(level))
        #     return jsonify(graph), 200
        #   except Exception as err:
        #     print(err, file=sys.stderr)
        #     return jsonify({'message': 'Error on generating graph'}), 500
          
        @self.app.route('/<username>/graph/<level>', methods=['GET'])
        def get_graph(username, level):
          try:
            graph = self.gitService.get_graph(username, int(level))
            return jsonify(graph), 200
          except Exception as err:
            print(err, file=sys.stderr)
            return jsonify({'message': 'Error on generating graph'}), 500
          
        @self.app.route('/search', methods=['POST'])
        def search():
          try:
            request_data = request.get_json()
            origin = request_data['origin']
            destiny = request_data['destiny']
            graph = request_data['graph']
            result = self.gitService.separation(origin, destiny, graph)
            return jsonify(result), 200
          except Exception as err:
            print(err, file=sys.stderr)
            return jsonify({'message': 'Error on searching'}), 500