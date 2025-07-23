# eventspec.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Map ChessTab event names to tk(inter) event detail values."""


class EventSpec:
    """Event detail values for ChessTab keyboard and pointer actions."""

    # Export PGN options.
    menu_database_export_games_cql = ("", "PGN CQL scan", "", 4)

    menu_position_partial = ("", "Query", "", 0)
    menu_position_show_query_engines = ("", "Show Query Engines", "", 11)
