# cqlinsert.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Widgets to insert Chess Query Language (ChessQL) statements."""
import tkinter
import tkinter.messagebox

from solentware_grid.core.dataclient import DataNotify

import chesstab.gui.displaytext
import chesstab.gui.cqledit
import chesstab.gui.cqlinsertbase
import chesstab.core.cqlstatement

from .cqldisplay import CQLDisplay


class CQLInsert(
    chesstab.gui.cqlinsertbase.CQLInsertBase,
    chesstab.gui.displaytext.ListGamesText,
    chesstab.gui.displaytext.InsertText,
    CQLDisplay,
    chesstab.gui.cqledit.CQLEdit,
    DataNotify,
):
    """Display ChessQL statement from database allowing insert."""

    def _process_and_set_cql_statement_list(self, event=None):
        """Display games with position matching edited ChessQL statement."""
        del event
        title = "List CQL Statement"
        self._clear_statement_tags()
        try:
            self.cql_statement.prepare_cql_statement(
                self.get_name_cql_statement_text()
            )
        except chesstab.core.cqlstatement.CQLStatementError as exc:
            tag_ranges = self.score.tag_ranges(self.TEXT_DATA)
            evaluator = self.cql_statement.query_container.evaluator
            if evaluator.error_location is not None:
                start = self.score.index(evaluator.error_location)
                if not tag_ranges or len(tag_ranges) > 2:
                    self.score.tag_add(self.ERROR_TAG, start)
                else:
                    self.score.tag_add(
                        self.ERROR_TAG,
                        start,
                        start + str(evaluator.error_length).join("+c"),
                    )
            tkinter.messagebox.showinfo(
                parent=self.ui.get_toplevel(),
                title=title,
                message=str(exc),
            )
            return "break"
        if tkinter.messagebox.YES != tkinter.messagebox.askquestion(
            parent=self.ui.get_toplevel(),
            title=title,
            message="CQL statement is valid\n\nRun and list games",
        ):
            return "break"
        try:
            self.refresh_game_list(ignore_sourceobject=True)
        except chesstab.core.cqlstatement.CQLStatementError as exc:
            tag_ranges = self.score.tag_ranges(self.TEXT_DATA)
            evaluator = self.cql_statement.query_container.evaluator
            if evaluator.error_location is not None:
                start = self.score.index(evaluator.error_location)
                if not tag_ranges or len(tag_ranges) > 2:
                    self.score.tag_add(self.ERROR_TAG, start)
                else:
                    self.score.tag_add(
                        self.ERROR_TAG,
                        start,
                        start + str(evaluator.error_length).join("+c"),
                    )
            tkinter.messagebox.showinfo(
                parent=self.ui.get_toplevel(),
                title=title,
                message=str(exc),
            )
        return "break"
