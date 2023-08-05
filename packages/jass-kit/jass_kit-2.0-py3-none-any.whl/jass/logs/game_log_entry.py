# HSLU
#
# Created by Thomas Koller on 7/31/2020
#
from datetime import datetime
from typing import List

from jass.game.const import DATE_FORMAT
from jass.game.game_state import GameState


class GameLogEntry:
    """
    Class to capture the information contained in match logs that are saved from real and simulated games
    and contain the match, the date and information about the players.
    """
    def __init__(self, game: GameState, date: datetime = None, player_ids: List[int] = None):
        """
        Game entry
        Args:
            game: a match state of a completed match
            date: the data when the match was played
            player_ids: information about the players
        """
        self.game = game
        self.date = date
        self.player_ids = player_ids

    def __eq__(self, other):
        return self.game == other.match and self.date == other.date and self.player_ids == other.player_ids

    def to_json(self) -> dict:
        """
        Convert to dict.

        Returns:
            dict containing the data
        """
        return dict(game=self.game.to_json(),
                    date=datetime.strftime(self.date, DATE_FORMAT),
                    player_ids=self.player_ids)

    @classmethod
    def from_json(cls, data):
        return GameLogEntry(game=GameState.from_json(data['match']),
                            date=datetime.strptime(data['date'], DATE_FORMAT),
                            player_ids=data['player_ids'])
