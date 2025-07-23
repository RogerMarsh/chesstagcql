# gamegrid.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Grids for listing details of games on chess database."""

import chesstab.gui.gamegrid
from chesstab.gui.gamerow import ChessDBrowGame
from chesstab.gui.positionrow import ChessDBrowPosition

from .gamelistgrid import GameListGrid


class PartialPositionGames(
    chesstab.gui.gamegrid.GameGridBaseAll,
    chesstab.gui.gamegrid.GameGridBasePosition,
    chesstab.gui.gamegrid.GameGridBasePartial,
    GameListGrid,
):
    """Customized GameListGrid for list of games matching a partial position.

    The grid is populated by a ChessQueryLanguageDS instance from the dpt.cqlds
    or basecore.cqlds modules.
    """

    def __init__(self, ui):
        """Extend with partial position grid definition and bindings.

        ui - container for user interface widgets and methods.

        """
        super().__init__(ui.position_partials_pw, ui)
        self.make_header(ChessDBrowGame.header_specification)
        self.__bind_on()
        self._set_initial_bindings()

    def bind_on(self):
        """Enable all bindings."""
        super().bind_on()
        self.__bind_on()

    def __bind_on(self):
        """Enable all bindings."""
        self._set_bindings_in__bind_on()

    def _edit_popup_entry(self):
        """Return event specification entry."""
        return ()

    def _bind_off_edit_entry(self):
        """Return event specification entry."""
        return ()

    def _bind_on_edit_entry(self):
        """Return event specification entry."""
        return ()


class GamePositionGames(
    chesstab.gui.gamegrid.GameGridBaseAll,
    chesstab.gui.gamegrid.GameGridBasePosition,
    chesstab.gui.gamegrid.GameGridBaseTransposition,
    GameListGrid,
):
    """Customized GameListGrid for list of games matching a game position.

    The grid is populated by a FullPositionDS instance from the
    dpt.fullpositionds or basecore.fullpositionds modules.
    """

    def __init__(self, ui):
        """Extend with position grid definition and bindings.

        ui - container for user interface widgets and methods.

        """
        super().__init__(ui.position_games_pw, ui)
        self.make_header(ChessDBrowPosition.header_specification)
        self.__bind_on()
        self._set_initial_bindings()

    def bind_on(self):
        """Enable all bindings."""
        super().bind_on()
        self.__bind_on()

    def __bind_on(self):
        """Enable all bindings."""
        self._set_bindings_in__bind_on()

    def _edit_popup_entry(self):
        """Return event specification entry."""
        return ()

    def _bind_off_edit_entry(self):
        """Return event specification entry."""
        return ()

    def _bind_on_edit_entry(self):
        """Return event specification entry."""
        return ()


class TagRosterGrid(
    chesstab.gui.gamegrid.GameGridBaseAll,
    chesstab.gui.gamegrid.GameGridBaseTagRoster,
    GameListGrid,
):
    """Customized GameListGrid for list of games on database.

    The grid is usually populated by a DataSource instance from the
    solentware_grid.core.dataclient module, either all games or by index or
    filter, but can be populated by a ChessQLGames instance from the dpt.cqlds
    or basecore.cqlds modules, when a selection rule is invoked.
    """

    def __init__(self, ui):
        """Extend with definition and bindings for games on database grid.

        ui - container for user interface widgets and methods.

        """
        super().__init__(ui.games_pw, ui)
        self.make_header(ChessDBrowGame.header_specification)
        self.__bind_on()
        self._set_initial_bindings()

    def bind_on(self):
        """Enable all bindings."""
        super().bind_on()
        self.__bind_on()

    def __bind_on(self):
        """Enable all bindings."""
        self._set_bindings_in__bind_on()

    def _edit_popup_entry(self):
        """Return event specification entry."""
        return ()

    def _bind_off_edit_entry(self):
        """Return event specification entry."""
        return ()

    def _bind_on_edit_entry(self):
        """Return event specification entry."""
        return ()
