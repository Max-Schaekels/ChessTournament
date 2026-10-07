class Match:
    def __init__(self, match_id, tournament, white_player, black_player, round_number, result="Not played"):
        self._id = match_id
        self._tournament = tournament
        self._white_player = white_player
        self._black_player = black_player
        self._round_number = round_number
        self.result = result

    @property
    def id(self):
        return self._id

    @property
    def tournament(self):
        return self._tournament

    @property
    def white_player(self):
        return self._white_player

    @property
    def black_player(self):
        return self._black_player

    @property
    def round_number(self):
        return self._round_number

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result):
        valid_results = {"Not played", "White wins", "Black wins", "Draw"}

        if result not in valid_results:
            raise ValueError(f"Invalid match result: {result}")

        self._result = result