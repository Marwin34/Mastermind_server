class Engine:
    def __init__(self):
        self.players = []

    def update(self):
        print(self.players)
        for player in self.players:
            commands = player['requests']
            for command in commands:
                if command['type'] == 'hi':
                    response = {'type': 'server_response',
                                'value': "Hi hi hello " + command['value'] + ", from server!"}
                    player['responses'].append(response)
            player['requests'] = []

    def get_players(self):
        return self.players
