# queryevaluator.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Run CQL program against games on database.

This module defines the QueryContainer class.  An instance of this class
runs the CQL program using the *.cql file and *.pgn file associated with
a database.  Both files are generated from the database as needed.
"""
import subprocess
import os
import re

import chesstab.core.cqlstatement

from ..core import enginecommands

# Search for items in response from CQL program.
_version_re = re.compile(rb"CQL version .+ Gady Costeff and Lewis Stiller\n")
_syntax_error_at_char_re = re.compile(
    rb"".join(
        (
            rb"(CQL syntax error:.*{Line\s(\d+),\sColumn\s(\d+)}.*\s",
            rb'(?:(?:"([^"]*)")?|[^\n]*)>)\n\n$',
        )
    ),
    flags=re.DOTALL,
)
_syntax_error_other_re = re.compile(rb"CQL syntax error:.*$", flags=re.DOTALL)
_game_count_re = re.compile(rb"\n(\d+) matches of (\d+) games in ")
_game_number_re = re.compile(rb"<(\d+)>")

# CQL counts games from 1 in the PGN file evaluated.  Most databases count
# records from 1 but some count from 0.  The PGN file generated from the
# database is constructed as if it were possible for the database to have a
# record 0 so always subtracting 1 from the CQL game number gives the
# database record number.  The PGN file has dummy games for all missing
# record numbers below the high record number, including record number 0
# for databases which never have this record number.
# If a database starts it's record numbers at n, n > 0, then n dummy games
# are at the start of the PGN file so it is always correct to subtract 1
# from the CQL game number to get the database record number.
CQL_GAME_NUMBER_OFFSET = 1


class QueryEvaluator:
    """The evaluator for a CQL statement."""

    def __init__(self):
        """Set details for root of node tree."""
        self.message = None
        self.default_text = None
        self.statement = None
        self.error_location = None
        self.error_length = None

    def find_command(self, database_file):
        """Set self.default_text to command to evaluate CQL statement.

        Set self.message if no suitable command is found.

        """
        self.default_text = None
        self.message = None
        commands = enginecommands.EngineCommands(database_file)
        try:
            for default, title, text in zip(*commands.read_pattern_engines()):
                del title
                if default:
                    self.default_text = text
                    break
        except FileNotFoundError:
            self.message = "".join(
                (
                    "Unable to pick query engine because '",
                    commands.filename,
                    "' does not exist",
                )
            )
        except IsADirectoryError:
            self.message = "".join(
                (
                    "Unable to pick query engine because '",
                    commands.filename,
                    "' is a directory not a file as expected",
                )
            )
        except SyntaxError:
            self.message = "".join(
                (
                    "Unable to pick query engine because '",
                    commands.filename,
                    "' gave a SyntaxError exception",
                )
            )
        except KeyError:
            self.message = "".join(
                (
                    "Unable to pick query engine because '",
                    commands.filename,
                    "' does not contain any",
                )
            )
        if self.default_text is None:
            self.message = "".join(
                (
                    "'",
                    commands.filename,
                    "' does not contain a default command",
                )
            )

    def verify_command_is_cql(self):
        """Run command with '-version' option and confirm response."""
        self.message = None
        try:
            completed = subprocess.run(
                [self.default_text, "--version"],
                capture_output=True,
                check=False,
            )
            if completed.returncode:
                self.message = "".join(
                    (
                        "Verification run of \n\n'",
                        self.default_text,
                        "'\n\ngave\n\n",
                        " ".join(("Returncode is", str(completed.returncode))),
                    )
                )
            if _version_re.match(completed.stdout) is None:
                self.message = "".join(
                    (
                        "Verification run of \n\n'",
                        self.default_text,
                        "'\n\ngave\n\n",
                        "Version not found verifying CQL",
                    )
                )
        except OSError as exc:
            self.message = "".join(
                (
                    "Verification run of \n\n'",
                    self.default_text,
                    "'\n\ncaused exception\n\n",
                    str(exc),
                )
            )

    def verify_cql_pqn_input_is_present(self, statement):
        """Return True if PGN input file is present."""
        self.message = None
        try:
            present = os.path.isfile(statement.pgn_filename)
        except FileNotFoundError:
            self.message = "".join(
                (
                    "Unable to run query because '",
                    statement.pgn_filename,
                    "' does not exist",
                )
            )
        except IsADirectoryError:
            self.message = "".join(
                (
                    "Unable to run query because '",
                    statement.pgn_filename,
                    "' is a directory not a file as expected",
                )
            )
        if not present:
            self.message = "".join(
                (
                    "Cannot run CQL command because '",
                    statement.pgn_filename,
                    "' does not exist",
                )
            )

    def write_cql_statement_file(self, query, statement):
        """Write query to CQL query file."""
        self.message = None
        try:
            with open(
                statement.cql_filename, mode="w", encoding="utf8"
            ) as file:
                file.write(query)
        except IsADirectoryError:
            self.message = "".join(
                (
                    "Cannot run CQL command because '",
                    statement.cql_filename,
                    "' is a directory",
                )
            )

    def parse_statement(self, statement):
        """Run CQL in a subprocess to parsee CQL query against PGN file."""
        self.message = None
        completed = subprocess.run(
            [
                self.default_text,
                "--parse",
                "--input",
                statement.pgn_filename,
                statement.cql_filename,
            ],
            capture_output=True,
            check=False,
        )
        if not completed.returncode:
            return
        error = _syntax_error_at_char_re.search(completed.stdout)
        if error is None:
            error = _syntax_error_other_re.search(completed.stdout)
            if error is not None:
                self.message = "".join(
                    (
                        "CQL run of \n\n'",
                        statement.cql_filename,
                        "'\n\nagainst\n\n'",
                        statement.pgn_filename,
                        "'\n\ncaused exception\n\n",
                        error.group().decode(),
                    )
                )
            else:
                self.message = "".join(
                    (
                        "CQL run of \n\n'",
                        statement.cql_filename,
                        "'\n\nagainst\n\n'",
                        statement.pgn_filename,
                        "'\n\ncaused exception\n\n",
                        completed.stdout.decode(),
                    )
                )
            return
        # CQL counts characters in line from 1 but tkinter counts from 0.
        # The first line in widget is line 4 when elided text is included
        # but is line 2 in the text given to CQL due to leading '\n' when
        # splitting title from query text.
        # Line 4 in widget starts with an elided character.
        # Better to save the CQL line and character location and convert
        # as needed closer to the widget tagging code.
        line = str(int(error.group(2).decode()) + 2)
        char_offset = 0 if line == "4" else 1
        self.error_location = ".".join(
            [line, str(int(error.group(3).decode()) - char_offset)]
        )
        if error.group(4) is not None:
            self.error_length = len(error.group(4).decode())
        self.message = "".join(
            (
                "Cannot run CQL command because\n\n'",
                error.group(1).decode(),
                "'\n\nis reported by CQL",
            )
        )

    def run_statement(self, statement, commit=True):
        """Run CQL in a subprocess to evaluate CQL query against PGN file."""
        self.message = None
        try:
            _run_statement(statement, self.default_text, commit=commit)
        except OSError as exc:
            self.message = "".join(
                (
                    "CQL run of \n\n'",
                    statement.cql_filename,
                    "'\n\nagainst\n\n'",
                    statement.pgn_filename,
                    "'\n\ncaused exception\n\n",
                    str(exc),
                )
            )
        except chesstab.core.cqlstatement.CQLStatementError as exc:
            self.message = "".join(
                (
                    "CQL run of \n\n'",
                    statement.cql_filename,
                    "'\n\nagainst\n\n'",
                    statement.pgn_filename,
                    "'\n\ncaused exception\n\n",
                    str(exc),
                )
            )


def _run_statement(statement, command, commit=True):
    """Run CQL in a subprocess to evaluate CQL query against PGN file."""
    # The text of query has already been written to file read by CQL
    # in subprocess, but the _description_string and _statement_string
    # attributes are still to be set like in process_statement().
    completed = subprocess.run(
        [
            command,
            "--showmatches",
            "--input",
            statement.pgn_filename,
            statement.cql_filename,
        ],
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        raise chesstab.core.cqlstatement.CQLStatementError(
            " ".join(("Returncode is", str(completed.returncode)))
        )
    if _version_re.match(completed.stdout) is None:
        raise chesstab.core.cqlstatement.CQLStatementError(
            "Version not found evaluating CQL"
        )
    games = _game_count_re.search(completed.stdout)
    if games is None:
        raise chesstab.core.cqlstatement.CQLStatementError(
            "Game counts not found evaluating CQL"
        )
    matches = int(games[1])
    game_count = int(games[2])
    recordset = statement.recordset
    cql_game_number_offset = CQL_GAME_NUMBER_OFFSET
    if commit:
        recordset.dbhome.start_transaction()
    try:
        high_record = recordset.dbhome.get_high_record_number(recordset.dbset)
        if high_record is None:
            raise chesstab.core.cqlstatement.CQLStatementError(
                " ".join(
                    (
                        str(game_count),
                        "total games found evaluating CQL but",
                        "no high record found on database",
                    )
                )
            )
        if game_count - cql_game_number_offset != high_record:
            raise chesstab.core.cqlstatement.CQLStatementError(
                " ".join(
                    (
                        str(game_count),
                        "total games found evaluating CQL but",
                        str(high_record),
                        "is high record number on database",
                    )
                )
            )
        for game in _game_number_re.finditer(completed.stdout):
            recordset.place_record_number(
                int(game.group(1)) - cql_game_number_offset
            )
        recordset &= recordset.dbhome.recordlist_ebm(recordset.dbset)
    finally:
        if commit:
            recordset.dbhome.backout()
    game_number_count = recordset.count_records()
    if matches != game_number_count:
        raise chesstab.core.cqlstatement.CQLStatementError(
            " ".join(
                (
                    str(matches),
                    "matching games found evaluating CQL but",
                    str(game_number_count),
                    "of these games are on database",
                )
            )
        )
