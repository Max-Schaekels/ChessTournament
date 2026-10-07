from datetime import date

from models.Player import Player
from models.Tournament import Tournament


class TournamentService:
    def __init__(self, tournaments=None):
        if tournaments is None:
            tournaments = []

        self._tournaments = tournaments
    @property
    def tournaments(self):
        return self._tournaments

    def add_tournament(self, tournament):
        self._tournaments.append(tournament)

    def remove_tournament(self, tournament):
        if tournament not in self._tournaments:
            raise ValueError(f'Tournament {tournament} not in the tournaments')
        if tournament.can_be_deleted() :
            self._tournaments.remove(tournament)
        else:
            raise ValueError(f"Tournament {tournament} can't be deleted because status is {tournament.status}")

    def last_ten_tournament(self):
        filtered_tournaments = [tournament for tournament in self._tournaments if tournament.status != "Completed"]
        sorted_tournaments = sorted(filtered_tournaments, key=lambda tournament : tournament.updated_at, reverse=True)
        return sorted_tournaments[:10]

    def display_tournaments(self):
        display_list = self.last_ten_tournament()
        #Name, Location, Number of registrants, Min/Max players, Categories, Min/Max ELO, Status, Registration deadline, Current round.
        for tournament in display_list:
            print(f"{tournament.name}: {tournament.status}")
            print(f"Location: {tournament.location}")
            print(f"Number of registrants : {len(tournament.players)}")
            print(f"Min players : {tournament.min_players}  -  Max players : {tournament.max_players}")
            print(f"Catégories : {tournament.categories}")
            print(f"Min ELO : {tournament.min_elo} - Max ELO : {tournament.max_elo}")
            print(f"Current round : {tournament.current_round}")
            print("")
            print("*****************************************************************")
            print("")

    def filter_tournaments(self, filter_name, value):

        match filter_name:
            case "name":
                filtered = [tournament for tournament in self._tournaments if value.lower() in tournament.name.lower()]

            case "location":
                filtered = [tournament for tournament in self._tournaments if
                            value.lower() in tournament.location.lower()]

            case "status":
                filtered = [tournament for tournament in self._tournaments if tournament.status == value]

            case "category":
                filtered = [tournament for tournament in self._tournaments if value in tournament.categories]

            case "min_elo":
                filtered = [tournament for tournament in self._tournaments if tournament.min_elo >= value]

            case "max_elo":
                filtered = [tournament for tournament in self._tournaments if tournament.max_elo <= value]

            case "women_only":
                filtered = [tournament for tournament in self._tournaments if tournament.women_only == value]

            case _:
                raise ValueError(f"Unknown filter: {filter_name}")

        return filtered

    def tournament_details(self):
        filters = {
            "name",
            "location",
            "status",
            "category",
            "min_elo",
            "max_elo",
            "women_only"
        }

        filter_name = input(f"Choose your filter for the search in {filters} : ")
        filter_value = input("Choose the value for the filter : ")

        if filter_name in {"min_elo", "max_elo"}:
            filter_value = int(filter_value)

        elif filter_name == "women_only":
            filter_value = filter_value.lower() in {"true", "yes", "y", "1"}

        target_tournaments = self.filter_tournaments(filter_name, filter_value)

        if not target_tournaments:
            print("Your search gives no result")
            return

        if len(target_tournaments) > 1:
            for index, tournament in enumerate(target_tournaments):
                print(f"{index} - {tournament.name} ({tournament.location})")

            choice = int(input("Choose a tournament : "))
            target_tournament = target_tournaments[choice]

        else:
            target_tournament = target_tournaments[0]

        print(f"{target_tournament.name}: {target_tournament.status}")
        print(f"Location: {target_tournament.location}")
        print(f"Number of registrants: {len(target_tournament.players)}")
        print(f"Min players: {target_tournament.min_players} - Max players: {target_tournament.max_players}")
        print(f"Categories: {target_tournament.categories}")
        print(f"Min ELO: {target_tournament.min_elo} - Max ELO: {target_tournament.max_elo}")
        print(f"Current round: {target_tournament.current_round}")

        print("Players:")
        for player in target_tournament.players:
            print(f"- {player.username}")

    def register_tournament(self, player, tournament):
        if tournament.status != "Waiting for players":
            print("You can't register in this tournament")
            return
        if player.gender == "male" and tournament.women_only:
            print("You can't register in this tournament, it's for women only")
            return

        if len(tournament.players) == tournament.max_players :
            print("The tournament is full")
            return

        if player in tournament.players:
            print("You are already registered")
            return

        if player.elo < tournament.min_elo:
            print("Your elo is too low for this tournament")
            return

        if player.elo > tournament.max_elo:
            print("Your elo is too high for this tournament")
            return

        today = date.today()

        age = today.year - player.date_of_birth.year - ((today.month, today.day) < (player.date_of_birth.month, player.date_of_birth.day))

        if age < 18:
            category = "Junior"
        elif age < 60:
            category = "Senior"
        else:
            category = "Veteran"

        if category not in tournament.categories:
            print(f"Your category {category} is not in the tournament categories : {tournament.categories}")
            return

        tournament.add_player(player)

    def unregister_tournament(self, player, tournament):
        if tournament.status != "Waiting for players":
            print("You can't unregister in this tournament")
            return

        if player not in tournament.players:
            print("You are not registered in this tournament")

        tournament.remove_player(player)

    def remove_tournament(self,tournament):
        if tournament not in self._tournaments:
            print("This tournament does not exist")

        if tournament.status != "Waiting for players":
            print("You can't unregister in this tournament, it's already started or finished")

        self._tournaments.remove(tournament)

    def start_tournament(self, tournament):
        if tournament.status != "Waiting for players":
            print("Tournament has already started")
            return False

        if len(tournament.players) < tournament.min_players:
            print("Not enough players to start the tournament")
            return False

        tournament.start_tournament()

        print("Tournament started")
        return True












