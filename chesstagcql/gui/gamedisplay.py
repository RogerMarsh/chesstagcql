# gamedisplay.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Widgets to display and edit game scores.

These four classes display PGN text for games in the main window: they are
used in the gamelistgrid module.

The GameDisplayBase class provides attributes and behaviour shared by the
GameDisplay, GameDisplayInsert, and GameDisplayEdit, classes.  It also provides
properties to support implementation of behaviour shared with the CQL*,
Repertoire*, and Query*, classes.

The GameDisplay, GameDisplayInsert, and GameDisplayEdit, classes are subclasses
of the relevant ShowPGN, InsertPGN, EditPGN, and DisplayPGN, classes from the
displaypgn module; to implement behaviour shared with all text widgets in the
main display (that includes widgets displaying text).

"""
from solentware_grid.core.dataclient import DataNotify

from solentware_bind.gui.bindings import Bindings

import chesstab.gui.gamedisplay
from chesstab.gui.game import Game
from chesstab.gui.gameedit import GameEdit
from chesstab.gui.display import Display
from .displaypgn import ShowPGN, InsertPGN, EditPGN, DisplayPGN


class GameDisplayBase(
    chesstab.gui.gamedisplay.GameDisplayBase,
    ShowPGN,
    DisplayPGN,
    Game,
    Display,
    Bindings,
    DataNotify,
):
    """Extend and link PGN game text to database."""


class GameDisplay(
    chesstab.gui.gamedisplay.GameDisplay,
    GameDisplayBase,
    Game,
    DataNotify,
):
    """Display a chess game from a database allowing delete and insert."""


class GameDisplayInsert(
    chesstab.gui.gamedisplay.GameDisplayInsert,
    InsertPGN,
    GameDisplayBase,
    GameEdit,
    DataNotify,
):
    """Display a chess game from a database allowing insert.

    GameEdit provides the widget and GameDisplayBase the database interface.
    """


class GameDisplayEdit(
    chesstab.gui.gamedisplay.GameDisplayEdit, EditPGN, GameDisplayInsert
):
    """Display a chess game from a database allowing edit and insert."""
