# HSLU
#
# Created by Thomas Koller on 27.07.20
#
import numpy as np

class DealingCardStrategy:
    """
    Abstract base class to deal for a match in the arena

    """
    def deal_cards(self, game_nr: int=0, total_nr_games=0) -> np.ndarray:
        """
        Args:
            game_nr: number of games played so far, starting with 1 for the first match
            total_nr_games: total number of games to be played, or 0 if not used

        """
        raise NotImplementedError
