# gamelistgrid.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Grids for listing details of games on chess database."""

import ast

from pgn_read.core.parser import PGN

import chesstab.gui.gamelistgrid
from .gamedisplay import GameDisplay, GameDisplayEdit


class GameListGrid(chesstab.gui.gamelistgrid.GameListGridReadOnly):
    """A DataGrid for lists of chess games.

    Subclasses provide navigation and extra methods appropriate to list use.

    """

    def make_display_widget(self, sourceobject):
        """Return a GameDisplay for sourceobject."""
        game = GameDisplay(
            master=self.ui.view_games_pw,
            ui=self.ui,
            items_manager=self.ui.game_items,
            itemgrid=self.ui.game_games,
            sourceobject=sourceobject,
        )
        game.set_position_analysis_data_source()
        game.collected_game = next(
            PGN(game_class=game.gameclass).read_games(
                ast.literal_eval(sourceobject.get_srvalue()[0])
            )
        )
        return game

    def make_edit_widget(self, sourceobject):
        """Return a GameDisplayEdit for sourceobject."""
        game = GameDisplayEdit(
            master=self.ui.view_games_pw,
            ui=self.ui,
            items_manager=self.ui.game_items,
            itemgrid=self.ui.game_games,
            sourceobject=sourceobject,
        )
        game.set_position_analysis_data_source()
        game.collected_game = next(
            PGN(game_class=game.gameclass).read_games(
                ast.literal_eval(sourceobject.get_srvalue()[0])
            )
        )
        return game
