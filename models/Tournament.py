from datetime import datetime

from models.Player import Player


class Tournament:
    def __init__(self, name: str, location, min_players, max_players, min_elo, max_elo, categories, women_only=False):
        self.name = name
        self.location = location

        if min_players < 2 or max_players > 32 or min_players > max_players:
            raise ValueError("Invalid players range")

        if min_elo < 0 or max_elo > 3000 or min_elo > max_elo:
            raise ValueError("Invalid ELO range")

        self._min_players = min_players
        self._max_players = max_players
        self._min_elo = min_elo
        self._max_elo = max_elo

        self.categories = categories
        self.women_only = women_only

        self._status = "Waiting for players"
        self._current_round = 0

        self._created_at = datetime.now()
        self._updated_at = self._created_at

        self._players = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = location

    @property
    def min_players(self):
        return self._min_players

    @property
    def max_players(self):
        return self._max_players

    @property
    def min_elo(self):
        return self._min_elo

    @property
    def max_elo(self):
        return self._max_elo

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, categories):
        valid_categories = {"Junior", "Senior", "Veteran"}

        if not categories:
            raise ValueError("At least one category is required")

        categories = set(categories)

        if not categories.issubset(valid_categories):
            raise ValueError(f"Invalid categories: {categories}")

        self._categories = categories

    @property
    def status(self):
        return self._status

    @property
    def women_only(self):
        return self._women_only

    @women_only.setter
    def women_only(self, women_only):
        if not isinstance(women_only, bool):
            raise ValueError("women_only must be a boolean")

        self._women_only = women_only

    @property
    def current_round(self):
        return self._current_round

    @property
    def created_at(self):
        return self._created_at

    @property
    def updated_at(self):
        return self._updated_at

    @property
    def players(self):
        return self._players

    def add_player(self, player):
        if not isinstance(player, Player):
            raise ValueError("Invalid player type")

        if player not in self._players:
            self._players.append(player)
            self._touch()

    def remove_player(self, player):
        if not isinstance(player, Player):
            raise ValueError("Invalid player type")

        if player in self._players:
            self._players.remove(player)
            self._touch()

    def _touch(self):
        self._updated_at = datetime.now()

    def can_be_deleted(self):
        return self.status == "Waiting for players"

    def next_round(self):
        self._current_round += 1
        self._touch()

    def start_tournament(self):
        if len(self.players) < self.min_players:
            print("The minimum player requirement is not reached, you can't start the tournament.")
            return False

        self._status = "In progress"
        self._current_round = 1
        self._touch()

        return True

    def complete_tournament(self):
        self._status = "Completed"
        self._touch()