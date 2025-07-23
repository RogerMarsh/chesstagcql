# displaypgn.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Provide classes which define set bindings and navigation methods.

Make subclasses of the classes provided by chesstab.displaytext and
override methods as needed to disable the event handlers intended for
write access methods to records.

"""
import chesstab.gui.displaypgn

from .displaytext import ShowText, DisplayText, EditText, InsertText


# Checking mro() output confirms it is safe to let chesstab.gui.displaypgn
# add chesstab.gui.scorepgn.ScorePGN to the ShowPGN class hierarchy.
class ShowPGN(chesstab.gui.displaypgn.ShowPGN, ShowText):
    """Provide methods to set bindinds and traverse visible items."""


class DisplayPGN(chesstab.gui.displaypgn.DisplayPGN, DisplayText):
    """Provide method to delete an item from database."""


class InsertPGN(chesstab.gui.displaypgn.InsertPGN, InsertText):
    """Provide methods to generate popup menus for inserting PGN scores."""


class EditPGN(chesstab.gui.displaypgn.EditPGN, EditText):
    """Provide methods to generate popup menus for editing PGN scores."""
