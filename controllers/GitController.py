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
            return jsonify({'message': 'Error on getting user followers'}), 404

        @self.app.route('/<username>/following', methods=['GET'])
        def get_following(username):
          try:
            all_following = self.gitService.get_all_following(username)
            return jsonify(all_following), 200
          except Exception as err:
            print(err, file=sys.stderr)
            return jsonify({'message': 'Error on getting user following'}), 404