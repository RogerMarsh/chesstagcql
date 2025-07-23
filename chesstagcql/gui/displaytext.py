# displaytext.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Provide classes which define binding and traversal methods for text.

Make subclasses of the classes provided by chesstab.displaytext and
override methods as needed to disable the event handlers intended for
write access methods to records.

"""
import chesstab.gui.displaytext


class ShowText(chesstab.gui.displaytext.ShowText):
    """Provide focus switching and visibility methods for text widgets."""

    def _create_database_submenu(self, menu):
        """Create and return popup submenu for database events."""
        return None


class DisplayText(chesstab.gui.displaytext.DisplayText):
    """Provide method to set database insert and delete event descriptions."""

    def _get_database_events(self):
        """Return event description tuple for PGN score database actions."""
        return ()


class InsertText(chesstab.gui.displaytext.InsertText):
    """Provide method which generates database insert event descriptions."""

    def _get_database_events(self):
        """Return event description tuple for PGN score database actions."""
        return ()


# Rather than just 'from chesstab.gui.displaytext import ListGamesText'
# which would be fine because no methods are overridden at present.
class ListGamesText(chesstab.gui.displaytext.ListGamesText):
    """Provide method which creates primary activity popup menu."""


class EditText(chesstab.gui.displaytext.EditText):
    """Provide method which generates database update event descriptions."""

    def _get_database_events(self):
        """Return event description tuple for PGN score database actions."""
        return ()
