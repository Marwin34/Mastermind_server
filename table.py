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

        if self.answers[self.player_1['nick']] == self.answers[self.player_2['nick']] == self.turn:
            self.compare_answer_with_code()

    def compare_answer_with_code(self):
        blacks = len(set(self.codes[self.player_1['nick']]) & set(self.answers[self.player_2['nick']]))

        response_value = []

        for i in range(4):
            if i < blacks:
                response_value.append('black')
            else:
                response_value.append('white')

        response = {
            'type': 'table_update',
            'value': response_value
        }

        self.player_2['responses'].append(response)

        blacks = len(set(self.codes[self.player_2['nick']]) & set(self.answers[self.player_1['nick']]))

        response_value = []

        for i in range(4):
            if i < blacks:
                response_value.append('black')
            else:
                response_value.append('white')

        response = {
            'type': 'table_update',
            'value': response_value
        }

        self.player_1['responses'].append(response)

        self.turn += 1


