######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# Dr. Jakob Prange                   #
# FAI Universität Augsburg           #
# WiSe 2024/25                       #
# Software Assignment                #
######################################

import hashlib


class Player:

    def __init__(self, name, password=None, password_hash=None):
        self.name = name
        if password != None:
            self.password_hash = Player.get_password_hash(password)
        elif password_hash != None:
            self.password_hash = password_hash

    def add_password(self, password):
        """Secures the player with a provided password.
        """
        self.password_hash = Player.get_password_hash(password)

    def validate_credentials(self, password) -> bool:
        """Checks the provided password against the password hash of the player.

        Returns:
            bool: True, if the provided password matches the hash or if the player has no password set.
        """
        if self.password_hash == None:
            return True

        return self.password_hash == Player.get_password_hash(password)

    def to_dict(self) -> dict:
        """Transforms the player data into a dictionary.
        """
        return {"name": self.name, "password_hash": self.password_hash}

    @staticmethod
    def from_dict(player_dict):
        """Creates a new `Player` instance from a dictionary.
        """
        return Player(name=player_dict["name"], password_hash=player_dict["password_hash"])

    @staticmethod
    def get_password_hash(password) -> str:
        """Transforms the provided password to a sha512 hash value.
        """
        return hashlib.sha512(password.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    '''
    write additional testing code here for things that don't work well as unit tests:
    '''
    player1 = Player('Yoshi')  # create new player
    player2 = Player('Peach')  # create new player
