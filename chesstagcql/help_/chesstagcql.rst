===================
ChessTagCQL - Notes
===================


This version of chesstagcql should run on any platform supported by Python 3.6 or later.  It is installed in Python's site-packages.


ChessTagCQL uses one of four database engines:

- Berkeley DB		(http://www.oracle.com)
- dptdb		(part of DPT from expired www.dptoolkit.com)
- sqlite3		(http://www.sqlite.org)
- apsw		(https://github.com/rogerbinns/apsw/)


 Sqlite3 is in the Python distribution and thus available for all supported platforms.

 apsw is a third party interface to sqlite3 which aims to provide a thinner wrapper of the sqlite3 API than Python's sqlite3 module.

 ChessTagQL is known to work with Berkeley DB versions 4.3.29, which recently ceased to be one of the versions ported to FreeBSD, and 5.3.28.

 dptdb is available for Microsoft Windows only.

 dptdb or Berkeley DB are used if installed with priority given to dptdb; and apsw is preferred over sqlite3 if installed.

 Support for Berkeley DB on Python 3 is available by installing the bsddb3 package from http://www.jcea.es.  A version of Berkeley DB supported by bsddb3 must be installed.

 bsddb3 is available also from http://pypi.python.org/pypi/bsddb3.

 Support for dptdb on Python3.3 is available by installing dpt3.0-dptdb-0.6.1 from http://www.solentware.co.uk.
