import random
from datetime import date

from models.Player import Player
from models.Tournament import Tournament
from services.TournamentService import TournamentService
from services.MatchService import MatchService



player1 = Player("Alice", "alice@test.com", date(2000, 5, 10), "female", 1500)
player2 = Player("Bob", "bob@test.com", date(1995, 8, 20), "male", 1400)
player3 = Player("Charlie", "charlie@test.com", date(2002, 3, 15), "male", 1600)
player4 = Player("Diana", "diana@test.com", date(1998, 11, 5), "female", 1550)



tournament = Tournament(
    "Chess Tournament Mons",
    "Mons",
    2,
    8,
    1000,
    2000,
    {"Senior"}
)


tournament_service = TournamentService()

tournament_service.add_tournament(tournament)

tournament_service.register_tournament(player1, tournament)
tournament_service.register_tournament(player2, tournament)
tournament_service.register_tournament(player3, tournament)
tournament_service.register_tournament(player4, tournament)


print("\n--- TOURNAMENT ---")
tournament_service.display_tournaments()



if tournament_service.start_tournament(tournament):

    match_service = MatchService(tournament)

    match_service.generate_round_robin()

    print("\n--- ALL MATCHES ---")

    for match in match_service.matches:
        print(
            f"Round {match.round_number} - "
            f"{match.white_player.username} VS {match.black_player.username}"
        )

    results = [
        "White wins",
        "White wins",
        "White wins",
        "Black wins",
        "Black wins",
        "Black wins",
        "Draw"
    ]


    while tournament.status == "In progress":

        print(f"\n--- ROUND {tournament.current_round} ---")

        current_matches = match_service.get_current_round_matches()

        for match in current_matches:

            print(
                f"{match.white_player.username} VS "
                f"{match.black_player.username}"
            )

            result = random.choice(results)

            match_service.update_match_result(match, result)

            print(f"Result: {result}")

        match_service.next_round()


    print("\n--- FINAL LEADERBOARD ---")

    match_service.display_leaderboard()