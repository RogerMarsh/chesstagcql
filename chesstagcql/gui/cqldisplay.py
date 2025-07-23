# cqldisplay.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Display Chess Query Language statements.

Add ability to display statements from database.
"""

import tkinter
import tkinter.messagebox

from solentware_grid.gui.dataedit import RecordEdit

import chesstab.gui.cqldisplaybase
import chesstab.core.cqlstatement
import chesstab.core.chessrecord


class CQLDisplay(chesstab.gui.cqldisplaybase.CQLDisplayBase):
    """Extend and link ChessQL statement to database.

    sourceobject - link to database.

    Attribute binding_labels specifies the order navigation bindings appear
    in popup menus.

    Method _insert_item_database allows records to be inserted into a database
    from any CQL widget.
    """

    def _insert_item_database(self, event=None):
        """Add ChessQL statement to database."""
        del event
        title = "Insert ChessQL Statement"
        if self.ui.partial_items.active_item is None:
            tkinter.messagebox.showinfo(
                parent=self.ui.get_toplevel(),
                title=title,
                message="No active CQL statement to insert into database.",
            )
            return

        # This should see if ChessQL statement with same name already exists,
        # after checking for database open, and offer option to insert anyway.
        if self.ui.database is None:
            tkinter.messagebox.showinfo(
                parent=self.ui.get_toplevel(),
                title=title,
                message="Cannot add CQL statement\n\nNo database open",
            )
            return

        datasource = self.ui.base_partials.get_data_source()
        if datasource is None:
            tkinter.messagebox.showinfo(
                parent=self.ui.get_toplevel(),
                title=title,
                message="".join(
                    (
                        "Cannot add CQL statement\n\n",
                        "Partial position list hidden",
                    )
                ),
            )
            return
        # Ignore self.cql_statement except for getting statement text
        # because ChessDBvaluePartial(CQLStatement, ...) will lead to a
        # database update.
        self.cql_statement.split_statement(
            "\n".join(
                (
                    self.get_tagged_text(self.TITLE_DATA),
                    self.get_tagged_text(self.TEXT_DATA),
                )
            )
        )
        if not self.cql_statement.get_name_text():
            tkinter.messagebox.showerror(
                parent=self.ui.get_toplevel(),
                title=title,
                message="".join(
                    (
                        "The '",
                        "CQL statement",
                        " has no name.\n\nPlease enter it's ",
                        "name as the first line of text.'",
                    )
                ),
            )
            return
        # The ChessDBvaluePartial with default __init__ arguments is not
        # appropriate here.
        updater = chesstab.core.chessrecord.ChessDBrecordPartial()
        updater.value = chesstab.core.chessrecord.ChessDBvaluePartial(
            opendatabase=self.ui.database,
            query_container_class=self.cql_statement.query_container_class,
        )
        try:
            updater.value.prepare_cql_statement(
                self.get_name_cql_statement_text()
            )
        except chesstab.core.cqlstatement.CQLStatementError as exc:
            tag_ranges = self.score.tag_ranges(self.TEXT_DATA)
            evaluator = updater.value.query_container.evaluator
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
            return
        try:
            updater.value.query_container.evaluator.run_statement(
                updater.value
            )
        except chesstab.core.cqlstatement.CQLStatementError as exc:
            tag_ranges = self.score.tag_ranges(self.TEXT_DATA)
            evaluator = updater.value.query_container.evaluator
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
            return
        if tkinter.messagebox.YES != tkinter.messagebox.askquestion(
            parent=self.ui.get_toplevel(),
            title=title,
            message="".join(
                (
                    "Confirm request to add CQL statement named:\n\n",
                    updater.value.get_name_text(),
                    "\n\nto database\n\n",
                )
            ),
        ):
            tkinter.messagebox.showinfo(
                parent=self.ui.get_toplevel(),
                title=title,
                message="Add CQL statement to database abandonned",
            )
            return
        editor = RecordEdit(updater, None)
        editor.set_data_source(source=datasource)
        updater.set_database(editor.get_data_source().dbhome)
        updater.key.recno = None  # 0
        editor.put()
        tkinter.messagebox.showinfo(
            parent=self.ui.get_toplevel(),
            title=title,
            message="".join(
                (
                    'CQL statement "',
                    updater.value.get_name_text(),
                    '" added to database',
                )
            ),
        )
