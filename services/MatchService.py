from models.Match import Match

class MatchService:
    def __init__(self, tournament):
        self._tournament = tournament
        self._matches = []

    def generate_round_robin(self):
        players = self._tournament.players.copy()

        if len(players) < 2:
            raise ValueError("Not enough players to generate matches")

        if len(players) % 2 != 0:
            players.append(None)

        number_of_players = len(players)
        number_of_rounds = number_of_players - 1
        half = number_of_players // 2

        rotation = players.copy()
        match_id = 1

        first_round_matches = []

        for round_number in range(1, number_of_rounds + 1):
            current_round = []

            for i in range(half):
                player1 = rotation[i]
                player2 = rotation[number_of_players - 1 - i]

                if player1 is None or player2 is None:
                    continue

                match = Match(match_id, self._tournament, player1, player2,round_number)

                self._matches.append(match)
                current_round.append(match)
                match_id += 1

            first_round_matches.append(current_round)

            rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]


        for index, round_matches in enumerate(first_round_matches):
            round_number = number_of_rounds + index + 1

            for first_match in round_matches:
                return_match = Match(match_id,self._tournament,first_match.black_player,first_match.white_player,round_number)

                self._matches.append(return_match)
                match_id += 1

        return self._matches

    def update_match_result(self, match, result):
        if match not in self._matches:
            print("Match not found in this tournament")
            return

        if match.round_number != self._tournament.current_round:
            print("You can only modify a match from the current round")
            return

        valid_results = {"Not played", "White wins", "Black wins", "Draw"}

        if result not in valid_results:
            print("Invalid match result")
            return

        match.result = result

    def get_current_round_matches(self):
        return [match for match in self._matches if match.round_number == self._tournament.current_round]

    def current_round_completed(self):
        current_matches = self.get_current_round_matches()

        return all(match.result != "Not played" for match in current_matches)

    def next_round(self):
        if not self.current_round_completed():
            print("All matches of the current round must be played first")
            return

        max_round = max(match.round_number for match in self._matches)

        if self._tournament.current_round >= max_round:
            self._tournament.complete_tournament()
            print("Tournament completed")
            return

        self._tournament.next_round()

        print(f"Round {self._tournament.current_round} started")

        def get_leaderboard(self):
            leaderboard = {}

            for player in self._tournament.players:
                leaderboard[player] = {
                    "played": 0,
                    "wins": 0,
                    "losses": 0,
                    "draws": 0,
                    "score": 0
                }

            for match in self._matches:
                if match.result == "Not played":
                    continue

                white = match.white_player
                black = match.black_player

                leaderboard[white]["played"] += 1
                leaderboard[black]["played"] += 1

                if match.result == "White wins":
                    leaderboard[white]["wins"] += 1
                    leaderboard[white]["score"] += 1
                    leaderboard[black]["losses"] += 1

                elif match.result == "Black wins":
                    leaderboard[black]["wins"] += 1
                    leaderboard[black]["score"] += 1
                    leaderboard[white]["losses"] += 1

                elif match.result == "Draw":
                    leaderboard[white]["draws"] += 1
                    leaderboard[black]["draws"] += 1
                    leaderboard[white]["score"] += 0.5
                    leaderboard[black]["score"] += 0.5

            return sorted(leaderboard.items(), key=lambda item: item[1]["score"], reverse=True)

        def display_leaderboard(self):
            leaderboard = self.get_leaderboard()

            for player, stats in leaderboard:
                print(f"{player.username}")
                print(f"Matches played: {stats['played']}")
                print(f"Wins: {stats['wins']}")
                print(f"Losses: {stats['losses']}")
                print(f"Draws: {stats['draws']}")
                print(f"Score: {stats['score']}")
                print("-----------------------------")
