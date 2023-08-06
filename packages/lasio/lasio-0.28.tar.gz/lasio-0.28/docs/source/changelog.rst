List of changes
===============================

Version 0.28 (12 September 2020)
--------------------------------
- Major re-write of reader code working towards LAS 3.0 support (#327; #347, #345, #353, #355, #358, #367, #368, #369)
- Fix #377 (writing "None" as the value instead of ""; #377)
- Fix #373 (enable GitHub Actions CI testing on MacOS, Windows, Ubuntu; #374, #387)
- Fix #363 (parse composite units such as "1000 lbf" correctly; #390)
- Fix #319 (allow skipping comment lines in data sections; #391)
- Avoid unnecessary exceptions on reading LAS 3.0 data sections (#385)
- Fix broken ReadTheDocs build

Version 0.27 (4 September 2020)
-------------------------------
- Fix #380 (install failed without git installed; #382)

Version 0.26 (31 August 2020)
-----------------------------
- This is the final version which works on Python 2.7 (#364)
- Fix #333 (header lines not parsed when colon is in description; #335)
- Fix #359 (sections not found when leading whitespace in line; #360, #361)
- Fix #350 (bug with NULL; #352)
- Fix #339 (0.1IN not recognised as index unit; #340, #349)
- Fix #31 (add command-line script to convert between LAS versions; #329)
- Fix #75 (add Cyrillic variant for metres; #330)
- Fix #326 (Support header-only LAS files--don't lose the last header section before a missing ~A section)
- Improve documentation regarding deleting items and curves (#315, #325)
- Add deprecation markers (#331)
- Align json.dumps and LASFile.to_json() (#328)
- Fixes and updates to setup.py relating to the adoption of setuptools_scm (#312, #317, #318)
- Clean up and background changes related to future LAS 3.0 support: #334, #337, #338, #341, #342, #346, #348, #372

Version 0.25.1 (1 May 2020)
-------------------------------------------
- Shift to setuptools_scm (#311)
- Fix #321 (EOF character causes error on read)
- Fix #182 (remove side-effect LASFile.write causing LASFile.version.VERS to change)
- Fix #310 (remove LASFile.metadata which was not working)

Version 0.25 (28 March 2020)
--------------------------------------------
- Add stack_curves() method to allow joining a set of curves into a 2D array (issue #284, PR #293)
- Add lasio.examples module (#296)
- Fix #278 (leading zeroes were being stripped from API/UWI numbers)
- Fix #286 (error on trying to write a file with one row of data)
- Fix #258 (do not catch Ctrl+C when reading file)
- Fix #292 (improve error checking for when trying to write non-2D data)
- Fix #277 (allow pathlib objects to lasio.read)
- Fix #264 (allow periods in mnemonics to be retained in specific cases)
- Fix #201 (adjust descr parsing in \~P section to allow times in the descr, see PR #298)
- Fix #302 (change in str(datetime) handling)
- Fixes to JSON output (#300, #303)
- Fix #304 (add column_fmt argument to LASFile.write method)

Version 0.24
--------------------------------------------
- Fix #256 (parse units in brackets and add index_unit kwarg)

Version 0.23
--------------------------------------------
- Fix #259 (error when encoding missing from URL response headers)
- Fix #262 (broken build due to cchardet dependency)

Version 0.22
--------------------------------------------
- Fix #252 (removing case sensitivity in index_unit checks)
- Fix #249 (fix bug producing df without converting to floats)
- Attempt to fix Lasso classification on GitHub

Version 0.21
--------------------------------------------
- Fix #236 and #237 (can now read ASCII in ~Data section)
- Fix #239 (Petrel can't read lasio output)

Version 0.20
--------------------------------------------
- Fix #233 (pickling error lost Curve.data during multiprocessing)
- Fix #226 (do not issue warning on empty ~Parameter section)
- Revised default behaviour to using null_policy='strict' (ref. #227)
- Fix #221 (depths > 10000 were being rounded by default)
- Fix #225 (file handle leaked if exception during parsing)

Version 0.19
--------------------------------------------
- Fix #223 (critical version/installation bug)

Version 0.18
--------------------------------------------
- Fix version numbering setup
- Fix #92 (can ignore blah blah lines in ~C section)
- Fix #209 (can now add curves with LASFile['mnemonic'] = [1, 2, 3])
- Fix #213 (LASFile.data is now a lazily generated property, with setter)
- Fix #218 (LASFile.append_curve was not adding data=[...] properly)
- Fix #216 (LASFile now raises KeyError for missing mnemonics)
- Fix #214 (first duplicate mnemonic when added was missing the :1)

Version 0.17
--------------------------------------------
- Add Appveyor continuous integration testing
- Add example notebook for how to use python logging module
- Fix #160 (add methods to LASFile for inserting curves)
- Fix #155 (implement del keyword for header items)
- Fix #142 (implement slicing for SectionItems)
- Fix #135 (UWI numbers losing their leading zeros)
- Fix #153 (fix SectionItems pprint repr in Python 3)
- Fix #81 (accept header items with missing colon)
- Fix #71 (add Docker build for lasio to DockerHub)
- Fix #210 (allow upper/lowercase standardization of mnemonics on read)
- Document recent additions (nearly up to date) (in Sphinx docs)

Version 0.16
--------------------------------------------
- Add read_policy and null_policy keywords - see documentation for details
- Fix bugs around files with missing ~V ~W ~P or ~C sections (#84 #85 #78)
- Fix #17 involving files with commas as a decimal mark
- Improve LASHeaderError traceback message
- Fix bug involving files with ~A but no data lines following
- Fix bug with blank line at start of file
- Fix bug involving missing or duplicate STRT, STOP and STEP mnemonics

Version 0.15.1
--------------------------------------------
- Major performance improvements with both memory and speed
- Major improvement to read parser, now using iteration
- Add ``LASFile.to_excel()`` and ``LASFile.to_csv()`` export methods
- Improve ``las2excelbulk.py`` script
- Published new and updated Sphinx documentation
- Improved character encoding handling when ``chardet`` not installed
- ``autodetect_encoding=True`` by default
- Allow reading of multiple non-standard header sections (#167, #168)
- Add flexibility in reading corrupted headers (``ignore_header_errors=True``)
- Add ability to avoid reading in data (``ignore_data=True``)
- Remove excessive debugging messages
- Fix bug #164 where ``FEET`` was not recognised as ``FT``
- Fix major globals() bug #141 affecting LASFile.add_curve
- Add command-line version script ``$ lasio`` to show version number.

Version 0.14 and 0.15 skipped due to broken PyPI upload.

Version 0.13
--------------------------------------------
- Other minor bug fixes inc inability to rename mnemonics in written LAS file.

Version 0.11.2
--------------------------------------------
- Fix bug with not correctly figuring out units for LASFile.write()
- Add ``LASFile.add_curve(CurveItem)`` method which automatically goes to the old
  method at ``LASFile.add_curve_raw(mnemonic=, data=, ...)`` if necessary, so it
  should be transparent to users

Version 0.11
--------------------------------------------
- Reorganise code into modules
- various

Version 0.10
--------------------------------------------
- Internal change to SectionItems for future LAS 3.0 support
- Added JSON encoder
- Added examples for using pandas DataFrame (.df attribute)
- LAS > Excel script refined (las2excel.py)

Version 0.9.1 (2015-11-11)
--------------------------------------------
 - pandas.DataFrame now as .df attribute, bugfix

Version 0.8 (2015-08-20)
--------------------------------------------
 - numerous bug fixes, API documentation added

Version 0.7 (2015-08-08)
--------------------------------------------
 - all tests passing on Python 2.6 through 3.4

Version 0.6 (2015-08-05)
--------------------------------------------
 - bugfixes and renamed from ``las_reader`` to ``lasio``

Version 0.5 (2015-08-01)
--------------------------------------------
 - Improvements to writing LAS files

Version 0.4 (2015-07-26)
--------------------------------------------
 - Improved handling of character encodings, other internal improvements

Version 0.3 (2015-07-23)
--------------------------------------------
 - Added Python 3 support, now reads LAS 1.2 and 2.0

Version 0.2 (2015-07-08)
--------------------------------------------
 - Tidied code and published on PyPI