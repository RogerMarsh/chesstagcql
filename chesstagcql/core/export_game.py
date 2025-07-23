# export_game.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess game exporters."""

import pgn_read

from chesstab.core import chessrecord, filespec
from chesstab.core.export_pgn_import_format import export_pgn_import_format

# PGN specification states ascii but these export functions used the
# default encoding before introduction of _ENCODING attribute.
# PGN files were read as "iso-8859-1" encoding when _ENCODING attribute
# was introduced.
# _ENCODING = "ascii"
# _ENCODING = "iso-8859-1"
_ENCODING = "utf-8"

strd = pgn_read.core.constants.SEVEN_TAG_ROSTER_DEFAULTS
STRDV = pgn_read.core.constants.DEFAULT_TAG_VALUE
PGNTR = pgn_read.core.constants.TAG_RESULT
_NULL_GAME_TEXT = "\n".join(
    (
        " ".join(
            [
                " ".join((t, strd.get(t, STRDV).join('""'))).join("[]")
                for t in pgn_read.core.constants.SEVEN_TAG_ROSTER
                if t != PGNTR
            ]
        ),
        " ".join((PGNTR, strd.get(PGNTR, STRDV).join('""'))).join("[]"),
        pgn_read.core.constants.DEFAULT_TAG_RESULT_VALUE,
        "",
    )
)
del strd, STRDV, PGNTR
del pgn_read


def export_all_games_for_cql_scan(database, filename):
    """Export all database games in a PGN inport format for CQL scan.

    A dummy game with no moves, '*' as result, and just the PGN Seven Tag
    Roster tags with the value representing unknown, is output in place
    of any game with errors.

    """
    if filename is None:
        return True
    instance = chessrecord.ChessDBrecordGame()
    instance.set_database(database)
    all_games_output = None
    no_games_output = True
    expected_record_number = 0
    database.start_read_only_transaction()
    valid_games = database.recordlist_ebm(filespec.GAMES_FILE_DEF)
    valid_games.remove_recordset(
        database.recordlist_all(
            filespec.GAMES_FILE_DEF, filespec.PGN_ERROR_FIELD_DEF
        )
    )
    try:
        cursor = database.database_cursor(
            filespec.GAMES_FILE_DEF,
            filespec.GAMES_FILE_DEF,
            recordset=valid_games,
        )
        try:
            with open(filename, "w", encoding=_ENCODING) as gamesout:
                current_record = cursor.first()
                while current_record:
                    try:
                        instance.load_record(current_record)
                    except StopIteration:
                        break
                    record_number = current_record[0]
                    while expected_record_number < record_number:
                        gamesout.write(_NULL_GAME_TEXT)
                        expected_record_number += 1
                    # Fix pycodestyle E501 (83 > 79 characters).
                    # black formatting applied with line-length = 79.
                    ivcg = instance.value.collected_game
                    if ivcg.is_pgn_valid_export_format():
                        gamesout.write(export_pgn_import_format(ivcg))
                        if all_games_output is None:
                            all_games_output = True
                            no_games_output = False
                    else:
                        gamesout.write(_NULL_GAME_TEXT)
                        if all_games_output:
                            if not no_games_output:
                                all_games_output = False
                    expected_record_number = record_number + 1
                    current_record = cursor.next()
        finally:
            cursor.close()
    finally:
        database.end_read_only_transaction()
    return all_games_output
