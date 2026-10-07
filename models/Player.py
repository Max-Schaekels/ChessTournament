class Player:
    def __init__(self, username, email, date_of_birth, gender : str, elo = 1200):
        self.username = username
        self._email = email
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.elo = elo

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def email(self):
        return self._email

    @property
    def date_of_birth(self):
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, date_of_birth):
        self._date_of_birth = date_of_birth

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        gender_set = {'male', 'female','other'}
        if gender.lower() not in gender_set:
            raise ValueError(f'Invalid gender {gender}')
        self._gender = gender.lower()

    @property
    def elo(self):
        return self._elo

    @elo.setter
    def elo(self, elo):
        if elo < 0 or elo > 3000:
            raise ValueError(f'Invalid elo {elo}')
        self._elo = elo
