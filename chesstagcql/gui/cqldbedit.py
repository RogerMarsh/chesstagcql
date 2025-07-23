# cqldbedit.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Customise edit toplevel to edit or insert ChessQL statement record.

ChessQL statements obey the syntax published for CQL version 6.0.1 (by Gady
Costeff).

"""
from chesstab.gui import _cqldbedit
from chesstab.core import filespec

from ..cql import querycontainer


class CQLDbEdit(_cqldbedit.CQLDbEditBase):
    """Edit ChessQL statement on database, or insert a new record.

    Customise the CQLDbEditBase edit and put methods for  evaluation of
    CQL statements by CQL program.
    """

    def prepare_cql_statement(self):
        """Fit CQLStatement class to CQLDbEdit class."""
        value = self.newobject.value
        opendatabase = self.datasource.dbhome
        value._recordset = opendatabase.recordlist_nil(filespec.GAMES_FILE_DEF)
        value._home_directory = opendatabase.home_directory
        value._database_file = opendatabase.database_file
        value._query_container_class = querycontainer.QueryContainer
