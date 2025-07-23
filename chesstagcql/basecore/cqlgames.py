# cqlgames.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Evaluate a ChessQL query using the CQL program."""

import chesstab.basecore.cqlbase


class ChessQLGames(chesstab.basecore.cqlbase.ChessQLBase):
    """Represent subset of games that match a Chess Query Language query.

    The query object has the required subset of games if the evaluation
    has been done.  Otherwise it is assumed returning an empty list of
    games based on games object should be returned.

    The arguments are those needed for an internal evaluation but the
    query object has the subset of games extracted from the response to
    running the CQL program.
    """

    def _get_games_matching_filters(self, query, games, commit=True):
        """Return query.recordset if it exists or empty list from games."""
        if query.query_container is None:
            query.prepare_cql_statement(query.get_name_statement_text())
        container = query.query_container
        if container and container.evaluator is not None:
            container.evaluator.run_statement(query, commit=commit)
        if query.recordset is not None:
            return query.recordset & games
        return games.dbhome.recordlist_nil(games.dbset)
