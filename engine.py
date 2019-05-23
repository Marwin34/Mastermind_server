from table import Table


def prepare_joined_table_message(player):
    response = {
        'type': 'joined_table',
        'value': True
    }

    player['responses'].append(response)


class Engine:
    def __init__(self):
        self.players = []

        self.waiters = []

        self.tables = []

    def update(self):
        print("Connected players: ", len(self.players), "current waiters: ", len(self.waiters), " current tables: ",
              len(self.tables))

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

                    if response_value:
                        self.waiters.append(player)

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
                elif command['type'] == 'waiting_for_opponent':
                    self.waiters.append(player)
                    response = {
                        'type': 'finding_table',
                        'value': True
                    }
                    player['responses'].append(response)
                elif command['type'] == 'code_init':
                    player['table'].set_up_code(player, command['value'])

            player['requests'] = []

        self.find_pairs()

    def find_pairs(self):
        while len(self.waiters) >= 2:
            table = Table(self.waiters[0], self.waiters[1])

            self.tables.append(table)

            self.waiters[0]['table'] = table
            prepare_joined_table_message(self.waiters[0])
            self.waiters.remove(self.waiters[0])
            self.waiters[0]['table'] = table
            prepare_joined_table_message(self.waiters[0])
            self.waiters.remove(self.waiters[0])

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
