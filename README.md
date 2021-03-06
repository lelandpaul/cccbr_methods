# CCCBR Methods Library

This is a [SQLAlchemy](https://sqlalchemy.org) + SQLite3 interface to the [CCCBR Methods Library](https://cccbr.github.io/methods-library/index.html).

```

>>> cccbr_methods.get('Double Norwich', stage=8).full_notation # Full place notation
'-.14.-.36.-.58.-.18.-.58.-.36.-.14.-.18'

```

# Installation

Install with `pip install cccbr_methods`, or download and run `python setup.py`.

# Searching for methods

The module provides two methods for searching the database: `get` and `search`; they differ only in that `get` returns the first result, while `search` returns a list of all results.

Both methods take a `search_string` argument; a method matches a search string if the string appears anywhere in `Method.title` (e.g. `cccbr_methods.search("Surprise")` will return all Surprise methods.) `get` will preferentially return exact matches of `search_string`.

```
>>> cccbr_methods.get('Double Norwich Court Bob Major') # Returns the first result
<Method Double Norwich Court Bob Major>

>>> cccbr_methods.search('Norwich Court') # Returns all results
[<Method Single Norwich Court Bob Major>, <Method Double Norwich Court Bob Major>, <Method Single Norwich Court Bob Caters>, <Method Double Norwich Court Bob Caters>, <Method Double Norwich Court Bob Royal>, <Method Double Norwich Court Bob Cinques>, <Method Double Norwich Court Bob Maximus>]

```

Other attributes can be passed as keyword arguments to further filter results:

```
>>> cccbr_methods.search('Double Norwich', stage=8) # Filter results further
[<Method Double Norwich Court Bob Major>]

```

As a convenience for more complicated searches, `cccbr_methods.query` returns a SQLAlchemy `Query` object suitable for further filtering.

All of these are also available directly from the `Method` object, e.g. `Method.get` is equivalent to `cccbr_methods.get`.


# Database columns

The database has two columns — one for methods, and one for significant performances. The database is deliberately sparse — many columns will be null if that information was not included in the original Library.

## methods

The `methods` table has the following columns:
- `id (Integer)` — The method ID assigned by the CCCBR library (with the 'm' prefixed stripped)
- `name (String)` — The method name, _excluding_ class & stage names
- `title (String)` — The method name, _including_ class & stage names
- `stage (Integer)`
- `leadhead (String)`
- `leadheadcode (String)`
- `symmetry (String)`
- `notation (String)` — The method place notation
- `falseness (String)` — The False Course Heads
- `extensionconstruction (String)`
- `classification (String)` — classification (e.g. 'Bob', 'Treble Bob', etc.)
- `trebledodging (Boolean)`
- `little (Boolean)`
- `differential (Boolean)`
- `lengthoflead (Integer)`
- `numberofhunts (Integer)`
- `huntbellpath (String)`
- `methodset_notes (String)` — the notes field included in the MethodSet
- `notes (String)` — the method notes from the library
- `pmmref, bnref, cbref, rwref, tdmmref (String)` — various reference types included in the Library

## performances

The `performaces` table has the following columns:
- `id (Integer)` — an autoincremented ID number (does not correspond to anything in the Library)
- `kind (String)` — one of `firstowerbellpeal, firsthandbellpeal, firstinclusionintowerbellpeal, firstinclusioninhandbellpeal, firstextent`
- `date (Date)`
- `society (String)`
- `town (String)`
- `county (String)`
- `building (String)`
- `address (String)`
- `country (String)`
- `room (String)`
- `region (String)`
- `method_id_fk (Integer; Foreign Key)`

# Object interface

This module provides two classes — one for methods, and one for the performances included in the CCCBR Library.

## Method

The `Method` class provides access to objects from the `methods` table in the database. All columns in the table are accessible as properties with the same name and type. The class additionally implements the following helper properties:

- `full_notation` — returns the full place notation (expanding any symmetry) as a string
- `full_notation_list` - returns the full place notation as a list of strings
- `performances` — returns a list of `Performance` objects corresponding to the performances linked to this method in the database

`Method` also provides an `__iter__` object over the columns in the table; in particular, `dict(<Method>)` will give you a dictionary of `{column_name: column_value}`.

## Performance

The `Performance` class provides access to objects from the `performances` table in the database. All columns in the table are accessible as properties with the same name and type. Additionally, a helper property `method` returns a `Method` object corresponding to the method linked to the performance in the database.

`Performance` also provides an `__iter__` object over the columns in the database; in particular, `dict(<Performance>)` will give you a dictionary of `{column_name: column_value}`.

# Updating the Database

While I make an effort to keep the database distributed with this package up to date, it may sometimes lag the CCCBR library. The module therefore provides the means update the database on demand. `cccbr_methods.update_database()` will download and parse the library, adding any new methods to the database. A CLI entry point is also provided: `update-cccbr-methods`.


# License information

This code is released under an MIT license. The CCCBR Methods database is copyright 2020 Central Council of Church Bell Ringers.
