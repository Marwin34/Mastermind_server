class Table:
    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2

        self.codes = {
            self.player_1['nick']: [None, None, None, None],
            self.player_2['nick']: [None, None, None, None]
        }

        self.answers = {
            self.player_1['nick']: [],
            self.player_2['nick']: []
        }

        self.codes_cnt = 0

        self.turn = 1

    def set_up_code(self, player, code):
        print(player)
        self.codes_cnt += 1
        self.codes[player['nick']] = code

        if self.codes_cnt == 2:
            response = {
                'type': 'start_game',
                'value': True
            }

            self.player_1['responses'].append(response)
            self.player_2['responses'].append(response)

    def update(self, player, code):
        if len(self.answers[player['nick']]) < self.turn:
            self.answers[player['nick']].append(code)

        if len(self.answers[self.player_1['nick']]) == len(self.answers[self.player_2['nick']]) == self.turn:
            self.compare_answer_with_code()

    def compare_answer_with_code(self):
        blacks_1 = 0
        for i in range(4):
            if self.codes[self.player_1['nick']][i] == \
                    self.answers[self.player_2['nick']][self.turn - 1][i]:
                blacks_1 += 1

        blacks_2 = 0
        for i in range(4):
            if self.codes[self.player_1['nick']][i] == \
                    self.answers[self.player_2['nick']][self.turn - 1][i]:
                blacks_2 += 1

        response_value_1 = []

        for i in range(4):
            if i < blacks_1:
                response_value_1.append('black')
            else:
                response_value_1.append('white')

        response_value_2 = []

        for i in range(4):
            if i < blacks_2:
                response_value_2.append('black')
            else:
                response_value_2.append('white')

        if blacks_1 == 4 or blacks_2 == 4:
            if blacks_1 == 4 and blacks_2 == 4:
                response_1 = {
                    'type': 'game_over',
                    'value': {
                        'turn': self.turn + 1,
                        'result': response_value_1,
                        'outcome': 'withdraw'
                    }
                }

                response_2 = response_1
            elif blacks_1 == 4:
                response_1 = {
                    'type': 'game_over',
                    'value': {
                        'turn': self.turn + 1,
                        'result': response_value_1,
                        'outcome': 'winner'
                    }
                }

                response_2 = {
                    'type': 'game_over',
                    'value': {
                        'turn': self.turn + 1,
                        'result': response_value_1,
                        'outcome': 'loser'
                    }
                }
            else:
                response_1 = {
                    'type': 'game_over',
                    'value': {
                        'turn': self.turn + 1,
                        'result': response_value_1,
                        'outcome': 'loser'
                    }
                }

                response_2 = {
                    'type': 'game_over',
                    'value': {
                        'turn': self.turn + 1,
                        'result': response_value_1,
                        'outcome': 'winner'
                    }
                }
        elif self.turn > 5:
            response_1 = {
                'type': 'game_over',
                'value': {
                    'turn': self.turn + 1,
                    'result': response_value_1,
                    'outcome': 'loser'
                }
            }

            response_2 = {
                'type': 'game_over',
                'value': {
                    'turn': self.turn + 1,
                    'result': response_value_1,
                    'outcome': 'loser'
                }
            }
        else:
            response_1 = {
                'type': 'table_update',
                'value': {
                    'turn': self.turn + 1,
                    'result': response_value_1,
                    'opponent': self.answers[self.player_1['nick']][self.turn - 1]
                }
            }

            response_2 = {
                'type': 'table_update',
                'value': {
                    'turn': self.turn + 1,
                    'result': response_value_2,
                    'opponent': self.answers[self.player_2['nick']][self.turn - 1]
                }
            }

        self.player_1['responses'].append(response_2)
        self.player_2['responses'].append(response_1)

        self.turn += 1
