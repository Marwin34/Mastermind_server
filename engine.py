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

                elif command['type'] == 'colors_match':
                    response = {
                        'type': 'server_response',
                        'value': command['value']
                        }
                    player['responses'].append(response)
                elif command['type'] == 'login':
                    response_value = self.add_unique_nick(player, command['value'])
                    response = {
                        'type': 'server_response',
                        'value': response_value
                    }
                    player['responses'].append(response)
                elif command['type'] == 'quit':

                    response = {
                        'type': 'quit',
                        'value': True
                    }
                    player['responses'].append(response)
                    player['to_remove'] = True
            player['requests'] = []

    def get_players(self):
        return self.players

    def add_unique_nick(self, player, nick):
        if player['nick'] != "":
            return False

        for target in self.players:
            if target['nick'] == nick:
                return False

        player['nick'] = nick

        return True

