# querycontainer.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Run CQL program against games on database.

This module defines the QueryContainer class.  An instance of this class
runs the CQL program using the *.cql file and *.pgn file associated with
a database.  Both files are generated from the database as needed.
"""

from . import queryevaluator


class QueryContainer:
    """The top level node for a CQL statement."""

    def __init__(self):
        """Set details for root of node tree."""
        self._evaluator = queryevaluator.QueryEvaluator()
        self._message = None

    @property
    def evaluator(self):
        """Return evaluator."""
        return self._evaluator

    @property
    def message(self):
        """Return error message or None."""
        return self._message

    def prepare_statement(self, statement, text):
        """Verify CQL statement is accepted by CQL program."""
        title_end = statement.split_statement(text)
        del title_end
        evaluator = self.evaluator
        evaluator.find_command(statement.database_file)
        if evaluator.message:
            self._message = evaluator.message
            return
        evaluator.verify_command_is_cql()
        if evaluator.message:
            self._message = evaluator.message
            return
        evaluator.verify_cql_pqn_input_is_present(statement)
        if evaluator.message:
            self._message = evaluator.message
            return
        evaluator.write_cql_statement_file(
            statement.get_statement_text(), statement
        )
        if evaluator.message:
            self._message = evaluator.message
            return
        evaluator.parse_statement(statement)
        if evaluator.message:
            self._message = evaluator.message
            return
