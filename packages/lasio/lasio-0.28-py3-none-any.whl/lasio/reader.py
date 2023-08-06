import codecs
import io
import logging
import os
import re
import traceback

import numpy as np

from . import defaults

# Convoluted import for StringIO in order to support:
#
# - Python 3 - io.StringIO
# - Python 2 (optimized) - cStringIO.StringIO
# - Python 2 (all) - StringIO.StringIO

try:
    import cStringIO as StringIO
except ImportError:
    try:  # cStringIO not available on this system
        import StringIO
    except ImportError:  # Python 3
        from io import StringIO
    else:
        from StringIO import StringIO
else:
    from StringIO import StringIO

from . import exceptions
from .las_items import HeaderItem, CurveItem, SectionItems, OrderedDict


logger = logging.getLogger(__name__)

URL_REGEXP = re.compile(
    r"^(?:http|ftp)s?://"  # http:// or https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}"
    r"\.?|[A-Z0-9-]{2,}\.?)|"  # (cont.) domain...
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


def check_for_path_obj(file_ref):
    """Check if file_ref is a pathlib.Path object.

    If file_ref is a pathlib.Path object, then return its absolute file
    path as a string so it will get processed as other string filenames.

    If pathlib is not available, do nothing and return file_ref.

    """
    try:
        from pathlib import Path
    except ImportError:
        return file_ref

    if isinstance(file_ref, Path):
        return file_ref.absolute().__str__()
    else:
        return file_ref


def open_file(file_ref, **encoding_kwargs):
    """Open a file if necessary.

    If ``autodetect_encoding=True`` then either ``cchardet`` or ``chardet``
    needs to be installed, or else an ``ImportError`` will be raised.

    Arguments:
        file_ref (file-like object, str): either a filename, an open file
            object, or a string containing the contents of a file.

    See :func:`lasio.reader.open_with_codecs` for keyword arguments that can be
    used here.

    Returns:
        tuple of an open file-like object, and the encoding that
        was used to decode it (if it were read from disk).

    """

    file_ref = check_for_path_obj(file_ref)

    encoding = None
    if isinstance(file_ref, str):  # file_ref != file-like object, so what is it?
        lines = file_ref.splitlines()
        first_line = lines[0]
        if URL_REGEXP.match(first_line):  # it's a URL
            logger.info("Loading URL {}".format(first_line))
            try:
                import urllib2

                response = urllib2.urlopen(first_line)
                encoding = response.headers.getparam("charset")

                tmp_str = response.read()
                tmp_list = tmp_str.splitlines()
                new_str = "\n".join(tmp_list)
                # file_ref = StringIO(response.read())
                file_ref = StringIO(new_str)
                logger.debug("Retrieved data had encoding {}".format(encoding))
            except ImportError:
                import urllib.request

                response = urllib.request.urlopen(file_ref)
                if response.headers.get_content_charset() is None:
                    if "encoding" in encoding_kwargs:
                        encoding = encoding_kwargs["encoding"]
                    else:
                        encoding = "utf-8"
                else:
                    encoding = response.headers.get_content_charset()
                # newline=None causes StringIO to use universal-newline:
                # Lines in the input can end in '\n', '\r', or '\r\n', and these are
                # translated into '\n' before being returned to the caller.
                file_ref = StringIO(response.read().decode(encoding), newline=None)
                logger.debug("Retrieved data decoded via {}".format(encoding))
        elif len(lines) > 1:  # it's LAS data as a string.
            file_ref = StringIO(file_ref)
        else:  # it must be a filename
            file_ref, encoding = open_with_codecs(first_line, **encoding_kwargs)
    return file_ref, encoding


def open_with_codecs(
    filename,
    encoding=None,
    encoding_errors="replace",
    autodetect_encoding=True,
    autodetect_encoding_chars=4000,
):
    """
    Read Unicode data from file.

    Arguments:
        filename (str): path to file

    Keyword Arguments:
        encoding (str): character encoding to open file_ref with, using
            :func:`io.open`.
        encoding_errors (str): 'strict', 'replace' (default), 'ignore' - how to
            handle errors with encodings (see
            `this section
            <https://docs.python.org/3/library/codecs.html#codec-base-classes>`__
            of the standard library's :mod:`codecs` module for more information)
        autodetect_encoding (str or bool): default True to use
            `chardet <https://github.com/chardet/chardet>`__/`cchardet
            <https://github.com/PyYoshi/cChardet>`__ to detect encoding.
            Note if set to False several common encodings will be tried but
            chardet won't be used.
        autodetect_encoding_chars (int/None): number of chars to read from LAS
            file for auto-detection of encoding.

    Returns:
        a unicode or string object

    This function is called by :func:`lasio.reader.open_file`.

    """
    if autodetect_encoding_chars:
        nbytes = int(autodetect_encoding_chars)
    else:
        nbytes = None

    # Forget [c]chardet - if we can locate the BOM we just assume that's correct.
    nbytes_test = min(32, os.path.getsize(filename))
    with open(filename, mode="rb") as test:
        raw = test.read(nbytes_test)
    if raw.startswith(codecs.BOM_UTF8):
        encoding = "utf-8-sig"
        autodetect_encoding = False

    # If BOM wasn't found...
    if (autodetect_encoding) and (not encoding):
        with open(filename, mode="rb") as test:
            if nbytes is None:
                raw = test.read()
            else:
                raw = test.read(nbytes)
        encoding = get_encoding(autodetect_encoding, raw)
        autodetect_encoding = False

    # Or if no BOM found & chardet not installed
    if (not autodetect_encoding) and (not encoding):
        encoding = adhoc_test_encoding(filename)
        if encoding:
            logger.info(
                "{} was found by ad hoc to work but note it might not"
                " be the correct encoding".format(encoding)
            )

    # Now open and return the file-like object
    logger.info(
        'Opening {} as {} and treating errors with "{}"'.format(
            filename, encoding, encoding_errors
        )
    )
    file_obj = io.open(filename, mode="r", encoding=encoding, errors=encoding_errors)
    return file_obj, encoding


def adhoc_test_encoding(filename):
    test_encodings = ["ascii", "windows-1252", "latin-1"]
    for i in test_encodings:
        encoding = i
        with io.open(filename, mode="r", encoding=encoding) as f:
            try:
                f.readline()
                break
            except UnicodeDecodeError:
                logger.debug("{} tested, raised UnicodeDecodeError".format(i))
                pass
            encoding = None
    return encoding


def get_encoding(auto, raw):
    """
    Automatically detect character encoding.

    Arguments:
        auto (str): auto-detection of character encoding - can be either
            'chardet', 'cchardet', False, or True (the latter will pick the
            fastest available option)
        raw (bytes): array of bytes to detect from

    Returns:
        A string specifying the character encoding.

    """
    if auto is True:
        try:
            import cchardet as chardet
        except ImportError:
            try:
                import chardet
            except ImportError:
                logger.debug(
                    "chardet or cchardet is recommended for automatic"
                    " detection of character encodings. Instead trying some"
                    " common encodings."
                )
                return None
            else:
                logger.debug("get_encoding Using chardet")
                method = "chardet"
        else:
            logger.debug("get_encoding Using cchardet")
            method = "cchardet"
    elif auto.lower() == "chardet":
        import chardet

        logger.debug("get_encoding Using chardet")
        method = "chardet"
    elif auto.lower() == "cchardet":
        import cchardet as chardet

        logger.debug("get_encoding Using cchardet")
        method = "cchardet"
    result = chardet.detect(raw)
    logger.debug(
        "{} method detected encoding of {} at confidence {}".format(
            method, result["encoding"], result["confidence"]
        )
    )
    return result["encoding"]


def find_sections_in_file(file_obj):
    """Find LAS sections in a file.

    Returns: a list of lists *(k, first_line_no, last_line_no, line]*.
        *file_pos* is the position in the *file_obj* in bytes,
        *first_line_no* is the first line number of the section (starting
        from zero), and *line* is the contents of the section title/definition
        i.e. beginning with ``~`` but stripped of beginning or ending whitespace
        or line breaks.

    """
    file_pos = int(file_obj.tell())
    starts = []
    ends = []
    line_no = 0
    line = file_obj.readline()
    # for i, line in enumerate(file_obj):
    while line:
        sline = line.strip().strip("\n")
        if sline.startswith("~"):
            starts.append((file_pos, line_no, sline))
            if len(starts) > 1:
                ends.append(line_no - 1)
        file_pos = int(file_obj.tell())
        line = file_obj.readline()
        line_no = line_no + 1

    ends.append(line_no)
    section_positions = []
    for j, (file_pos, first_line_no, sline) in enumerate(starts):
        section_positions.append((file_pos, first_line_no, ends[j], sline))
    return section_positions


def determine_section_type(section_title):
    """Return the type of the LAS section based on its title

        >>> determine_section_type("~Curves Section")
        "Header"
        >>> determine_section_type("~ASCII")
        "Data"

    Returns: bool

    """
    stitle = section_title.strip().strip("\n")
    if stitle[:2] == "~A":
        return "Data"
    elif stitle[:2] == "~O":
        return "Header (other)"
    # This is las3 transitional code till data parsing is robust for ~A and
    # '_Data' sections
    elif re.search("_Data", stitle):
        return "Las3_Data"
    else:
        return "Header items"


def read_file_contents(
    file_obj, regexp_subs, value_null_subs, ignore_data=False, remove_line_filter="#"
):
    """Read file contents into memory.

    Arguments:
        file_obj (open file-like object)

    Keyword Arguments:
        null_subs (bool): True will substitute ``numpy.nan`` for invalid values
        ignore_data (bool): if True, do not read in the numerical data in the
            ~ASCII section
        remove_line_filter (str, func): string or function for removing/ignoring lines
            in the data section e.g. a function which accepts a string (a line from the
            data section) and returns either True (do not parse the line) or False
            (parse the line). If this argument is a string it will instead be converted
            to a function which rejects all lines starting with that value e.g. ``"#"``
            will be converted to ``lambda line: line.strip().startswith("#")``

    Returns:
        OrderedDict

    I think of the returned dictionary as a "raw section". The keys are
    the first line of the LAS section, including the tilde. Each value is
    a dict with either::

        {"section_type": "header",
         "title": str,               # title of section (including the ~)
         "lines": [str, ],           # a list of the lines from the lAS file
         "line_nos": [int, ]         # line nos from the original file
         }

    or::

        {"section_type": "data",
         "title": str,              # title of section (including the ~)
         "start_line": int,         # location of data section (the title line)
         "ncols": int,              # no. of columns on first line of data,
         "array": ndarray           # 1-D numpy.ndarray,
         }

    """
    sections = OrderedDict()
    sect_lines = []
    sect_line_nos = []
    sect_title_line = None
    section_exists = False

    for i, line in enumerate(file_obj):
        logger.debug("Reading line {i}: {line}".format(i=i, line=line.strip("\n")))
        line = line.strip()
        if not line:
            continue
        if line.upper().startswith("~A"):
            logger.debug(
                "Line {i}: start of data section {line}".format(
                    i=i, line=line.strip("\n")
                )
            )

            # HARD CODED FOR VERSION 1.2 and 2.0; needs review for 3.0
            # We have finished looking at the metadata and need
            # to start reading numerical data.

            if not sect_title_line is None:
                sections[sect_title_line] = {
                    "section_type": "header",
                    "title": sect_title_line,
                    "lines": sect_lines,
                    "line_nos": sect_line_nos,
                }
                sect_lines = []
                sect_line_nos = []

            if not ignore_data:
                try:
                    data = read_data_section_iterative(
                        file_obj,
                        regexp_subs,
                        value_null_subs,
                        remove_line_filter=remove_line_filter,
                    )
                except KeyboardInterrupt:
                    raise
                except:
                    raise exceptions.LASDataError(
                        traceback.format_exc()[:-1]
                        + " in data section beginning line {}".format(i + 1)
                    )
                sections[line] = {
                    "section_type": "data",
                    "start_line": i,
                    "title": line,
                    "array": data,
                }
                logger.debug('Data section ["array"].shape = {}'.format(data.shape))

            section_exists = False
            break

        elif line.startswith("~"):
            logger.debug(
                "Line {i}: start of header section {line}".format(
                    i=i, line=line.strip("\n")
                )
            )
            if section_exists:
                # We have ended a section and need to start the next
                if not sect_title_line is None:
                    sections[sect_title_line] = {
                        "section_type": "header",
                        "title": sect_title_line,
                        "lines": sect_lines,
                        "line_nos": sect_line_nos,
                    }
                    sect_lines = []
                    sect_line_nos = []
            else:
                # We are entering into a section for the first time
                section_exists = True
                pass
            sect_title_line = line  # either way... this is the case.

        else:
            # We are in the middle of a section.
            if not line.startswith("#"):  # ignore commented-out lines.. for now.
                sect_lines.append(line)
                sect_line_nos.append(i + 1)

    # If the file had header data only, and is truncated before the ~A section
    # we need to save the last header section.
    if section_exists and not sect_title_line is None:
        sections[sect_title_line] = {
            "section_type": "header",
            "title": sect_title_line,
            "lines": sect_lines,
            "line_nos": sect_line_nos,
        }

    # Find the number of columns in the data section(s). This is only
    # useful if WRAP = NO, but we do it for all since we don't yet know
    # what the wrap setting is.

    for section in sections.values():
        if section["section_type"] == "data":
            section["ncols"] = None
            file_obj.seek(0)
            for i, line in enumerate(file_obj):
                if i == section["start_line"] + 1:
                    for pattern, sub_str in regexp_subs:
                        line = re.sub(pattern, sub_str, line)
                    section["ncols"] = len(line.split())
                    break
    return sections


def convert_remove_line_filter(filt):
    """Ensure that the line filter is a function.

    Arguments:
        filt (str, func): string or function for removing/ignoring lines
            in the data section e.g. a function which accepts a string (a line from the
            data section) and returns either True (do not parse the line) or False
            (parse the line). If this argument is a string it will instead be converted
            to a function which rejects all lines starting with that value e.g. ``"#"``
            will be converted to ``lambda line: line.strip().startswith("#")``

    Returns: function which takes a string (a data section line) and returns True
        or False.

    """
    if isinstance(filt, str):
        value = str(filt)
        filt = lambda line: line.strip().startswith(value)
    return filt


def inspect_data_section(file_obj, line_nos, regexp_subs, remove_line_filter="#"):
    """Determine how many columns there are in the data section.

    Arguments:
        file_obj: file-like object open for reading at the beginning of the section
        line_nos (tuple): the first and last line no of the section to read
        regexp_subs (list): each item should be a tuple of the pattern and
            substitution string for a call to re.sub() on each line of the
            data section. See defaults.py READ_SUBS and NULL_SUBS for examples.
        remove_line_filter (str, func): string or function for removing/ignoring lines
            in the data section e.g. a function which accepts a string (a line from the
            data section) and returns either True (do not parse the line) or False
            (parse the line). If this argument is a string it will instead be converted
            to a function which rejects all lines starting with that value e.g. ``"#"``
            will be converted to ``lambda line: line.strip().startswith("#")``

    Returns: integer number of columns or -1 where they are different.

    """
    remove_line_filter = convert_remove_line_filter(remove_line_filter)

    line_no = line_nos[0]
    title_line = file_obj.readline()

    item_counts = []

    for i, line in enumerate(file_obj):
        line_no = line_no + 1
        line = line.strip("\n").strip()
        if remove_line_filter(line):
            continue
        else:
            for pattern, sub_str in regexp_subs:
                line = re.sub(pattern, sub_str, line)
            n_items = len(line.split())
            logger.debug(
                "Line {}: {} items counted in '{}'".format(line_no + 1, n_items, line)
            )
            item_counts.append(n_items)
            if (line_no == line_nos[1]) or (i >= 20):
                break

    try:
        assert len(set(item_counts)) == 1
    except AssertionError:
        return -1
    else:
        return item_counts[0]


def read_data_section_iterative(
    file_obj, line_nos, regexp_subs, value_null_subs, remove_line_filter
):
    """Read data section into memory.

    Arguments:
        file_obj: file-like object open for reading at the beginning of the section
        line_nos (tuple): the first and last line no of the section to read
        regexp_subs (list): each item should be a tuple of the pattern and
            substitution string for a call to re.sub() on each line of the
            data section. See defaults.py READ_SUBS and NULL_SUBS for examples.
        value_null_subs (list): list of numerical values to be replaced by
            numpy.nan values.
        remove_line_filter (str or func): string or function for removing/ignoring lines
            in the data section e.g. a function which accepts a string (a line from the
            data section) and returns either True (do not parse the line) or False
            (parse the line). If this argument is a string it will instead be converted
            to a function which rejects all lines starting with that value e.g. ``"#"``
            will be converted to ``lambda line: line.strip().startswith("#")``


    Returns:
        A 1-D numpy ndarray.

    """

    remove_line_filter = convert_remove_line_filter(remove_line_filter)

    title = file_obj.readline()

    def items(f, start_line_no, end_line_no):
        line_no = start_line_no
        for line in f:
            line_no += 1
            logger.debug(
                "Line {}: reading data '{}'".format(
                    line_no + 1, line.strip("\n").strip()
                )
            )
            if remove_line_filter(line):
                continue
            else:
                for pattern, sub_str in regexp_subs:
                    line = re.sub(pattern, sub_str, line)
                line = line.replace(chr(26), "")
                for item in line.split():
                    try:
                        yield np.float64(item)
                    except ValueError:
                        yield item
                if line_no == end_line_no:
                    break

    array = np.array(
        [i for i in items(file_obj, start_line_no=line_nos[0], end_line_no=line_nos[1])]
    )
    for value in value_null_subs:
        array[array == value] = np.nan
    return array


def get_substitutions(read_policy, null_policy):
    """Parse read and null policy definitions into a list of regexp and value
    substitutions.

    Arguments:
        read_policy (str, list, or substitution): either (1) a string defined in
            defaults.READ_POLICIES; (2) a list of substitutions as defined by
            the keys of defaults.READ_SUBS; or (3) a list of actual substitutions
            similar to the values of defaults.READ_SUBS. You can mix (2) and (3)
            together if you want.
        null_policy (str, list, or sub): as for read_policy but for
            defaults.NULL_POLICIES and defaults.NULL_SUBS

    Returns:
        regexp_subs, value_null_subs, version_NULL - two lists and a bool.
        The first list is pairs of regexp patterns and substrs, and the second
        list is just a list of floats or integers. The bool is whether or not
        'NULL' was located as a substitution.

    """
    regexp_subs = []
    numerical_subs = []
    version_NULL = False

    for policy_typ, policy, policy_subs, subs in (
        ("read", read_policy, defaults.READ_POLICIES, defaults.READ_SUBS),
        ("null", null_policy, defaults.NULL_POLICIES, defaults.NULL_SUBS),
    ):
        try:
            is_policy = policy in policy_subs
        except TypeError:
            is_policy = False
        if is_policy:
            logger.debug('using {} policy of "{}"'.format(policy_typ, policy))
            all_subs = []
            for sub in policy_subs[policy]:
                logger.debug("adding substitution {}".format(sub))
                if sub in subs:
                    all_subs += subs[sub]
                if sub == "NULL":
                    logger.debug("located substition for LAS.version.NULL as True")
                    version_NULL = True
        else:
            all_subs = []
            for item in policy:
                if item in subs:
                    all_subs += subs[item]
                    if item == "NULL":
                        logger.debug(
                            "located substitution for LAS.version.NULL as True"
                        )
                        version_NULL = True
                else:
                    all_subs.append(item)
        for item in all_subs:
            try:
                iter(item)
            except TypeError:
                logger.debug("added numerical substitution: {}".format(item))
                numerical_subs.append(item)
            else:
                logger.debug(
                    'added regexp substitution: pattern={} substr="{}"'.format(
                        item[0], item[1]
                    )
                )
                regexp_subs.append(item)
    numerical_subs = [n for n in numerical_subs if not n is None]

    return regexp_subs, numerical_subs, version_NULL


def parse_header_items_section(
    file_obj,
    line_nos,
    version,
    ignore_header_errors=False,
    mnemonic_case="preserve",
    ignore_comments=("#",),
):
    """Parse a header section dict into a SectionItems containing HeaderItems.

    Arguments:
        file_obj: file-like object open for reading at the beginning of the section
        line_nos (tuple): the first and last line no of the section to read
        version (float): either 1.2 or 2.0

    Keyword Arguments:
        ignore_header_errors (bool): if True, issue HeaderItem parse errors
            as :func:`logging.warning` calls instead of a
            :exc:`lasio.exceptions.LASHeaderError` exception.
        mnemonic_case (str): 'preserve': keep the case of HeaderItem mnemonics
                             'upper': convert all HeaderItem mnemonics to uppercase
                             'lower': convert all HeaderItem mnemonics to lowercase
        ignore_comments (False, True, or list): ignore lines starting with these
            characters; by default True as '#'.

    Returns:
        :class:`lasio.SectionItems`

    """
    line_no = line_nos[0]
    title = file_obj.readline()
    title = title.strip("\n").strip()
    logger.debug("Line {}: Section title parsed as '{}'".format(line_no + 1, title))

    parser = SectionParser(title, version=version)

    section = SectionItems()
    assert mnemonic_case in ("upper", "lower", "preserve")
    if not mnemonic_case == "preserve":
        section.mnemonic_transforms = True

    for i, line in enumerate(file_obj):
        line_no = line_no + 1
        line = line.strip("\n").strip()
        if not line:
            logger.debug("Line {}: empty, ignoring".format(line_no + 1))
        elif line[0] in ignore_comments:
            logger.debug(
                "Line {}: treating as a comment and ignoring: '{}'".format(
                    line_no + 1, line
                )
            )
        else:
            # We have arrived at a new section so break and return the previous
            # section's object.
            if line.startswith("~"):
                break
            try:
                values = read_line(line, section_name=parser.section_name2)
            except:
                message = 'Line {} (section {}): "{}"'.format(line_no + 1, title, line)
                if ignore_header_errors:
                    logger.warning(message)
                else:
                    raise exceptions.LASHeaderError(message)
            else:
                if mnemonic_case == "upper":
                    values["name"] = values["name"].upper()
                elif mnemonic_case == "lower":
                    values["name"] = values["name"].lower()
                item = parser(**values)
                logger.debug("Line {}: parsed as {}".format(line_no + 1, item))
                section.append(item)
        if line_no == line_nos[1]:
            break

    return section


class SectionParser(object):

    """Parse lines from header sections.

    Arguments:
        title (str): title line of section. Used to understand different
            order formatting across the special sections ~C, ~P, ~W, and ~V,
            depending on version 1.2 or 2.0.

    Keyword Arguments:
        version (float): version to parse according to. Default is 1.2.

    """

    def __init__(self, title, version=1.2):
        las3_section_indicators = ["_DATA", "_PARAMETER", "_DEFINITION"]

        is_like_las3_section = any(
            [section_str in title.upper() for section_str in las3_section_indicators]
        )

        # On the first call to SectionParser ~Version hasn't been parsed.  So
        # the version number will report the default. Although the ~Version
        # section is supposed to be the first section, there can be las files
        # in the wild that don't have the ~Version or doesn't have it first. In
        # those cases a Las3 file would end up parsed as a Las2 file or
        # partially parsed as a Las2 file.
        if version == 3.0 and is_like_las3_section:
            self.func = self.metadata
            self.section_name2 = title
            self.default_order = "value:descr"
            self.orders = {}
        elif title.upper().startswith("~C"):
            self.func = self.curves
            self.section_name2 = "Curves"
        elif title.upper().startswith("~P"):
            self.func = self.params
            self.section_name2 = "Parameter"
        elif title.upper().startswith("~W"):
            self.func = self.metadata
            self.section_name2 = "Well"
        elif title.upper().startswith("~V"):
            self.func = self.metadata
            self.section_name2 = "Version"
        else:
            logger.info("Unknown section name {}".format(title.upper()))
            self.func = self.metadata
            self.section_name2 = title
            self.default_order = "value:descr"
            self.orders = {}

        self.version = version
        self.section_name = title

        defs = defaults.ORDER_DEFINITIONS

        if self.section_name2 in defs[self.version]:
            section_orders = defs[self.version][self.section_name2]
            self.default_order = section_orders[0]  #
            self.orders = {}
            for order, mnemonics in section_orders[1:]:
                for mnemonic in mnemonics:
                    self.orders[mnemonic] = order

    def __call__(self, **keys):
        """Return the correct object for this type of section.

        Refer to :meth:`lasio.reader.SectionParser.metadata`,
        :meth:`lasio.reader.SectionParser.params`, and
        :meth:`lasio.reader.SectionParser.curves` for the methods actually
        used by this routine.

        Keyword arguments should be the key:value pairs returned by
        :func:`lasio.reader.read_header_line`.

        """
        item = self.func(**keys)
        return item

    def num(self, x, default=None):
        """Attempt to parse a number.

        Arguments:
            x (str, int, float): potential number
            default (int, float, None): fall-back option

        Returns:
            int, float, or **default** - from most to least preferred types.

        """
        if default is None:
            default = x

        # in case it is a string.
        try:
            pattern, sub = defaults.READ_SUBS["comma-decimal-mark"][0]
            x = re.sub(pattern, sub, x)
        except:
            pass

        try:
            return np.int(x)
        except:
            try:
                x = np.float(x)
            except:
                return default
        if np.isfinite(x):
            return x
        else:
            return default

    def strip_brackets(self, x):
        x = x.strip()
        if len(x) >= 2:
            if (x[0] == "[" and x[-1] == "]") or (x[0] == "(" and x[-1] == ")"):
                return x[1:-1]
        return x

    def metadata(self, **keys):
        """Return HeaderItem correctly formatted according to the order
        prescribed for LAS v 1.2 or 2.0 for the ~W section.

        Keyword arguments should be the key:value pairs returned by
        :func:`lasio.reader.read_header_line`.

        """
        # number_strings: fields that shouldn't be converted to numbers
        number_strings = ["API", "UWI"]

        key_order = self.orders.get(keys["name"], self.default_order)

        value = ""
        descr = ""

        if key_order == "value:descr":
            value = keys["value"]
            descr = keys["descr"]
        elif key_order == "descr:value":
            value = keys["descr"]
            descr = keys["value"]

        if keys["name"].upper() not in number_strings:
            value = self.num(value)

        item = HeaderItem(
            keys["name"],  # mnemonic
            self.strip_brackets(keys["unit"]),  # unit
            value,  # value
            descr,  # descr
        )
        return item

    def curves(self, **keys):
        """Return CurveItem.

        Keyword arguments should be the key:value pairs returned by
        :func:`lasio.reader.read_header_line`.

        """
        item = CurveItem(
            keys["name"],  # mnemonic
            self.strip_brackets(keys["unit"]),  # unit
            keys["value"],  # value
            keys["descr"],  # descr
        )
        return item

    def params(self, **keys):
        """Return HeaderItem for ~P section (the same between 1.2 and 2.0 specs)

        Keyword arguments should be the key:value pairs returned by
        :func:`lasio.reader.read_header_line`.

        """
        return HeaderItem(
            keys["name"],  # mnemonic
            self.strip_brackets(keys["unit"]),  # unit
            self.num(keys["value"]),  # value
            keys["descr"],  # descr
        )


def read_line(*args, **kwargs):
    """Retained for backwards-compatibility.

    See :func:`lasio.reader.read_header_line`.

    """
    return read_header_line(*args, **kwargs)


def read_header_line(line, pattern=None, section_name=None):
    """Read a line from a LAS header section.

    The line is parsed with a regular expression -- see LAS file specs for
    more details, but it should basically be in the format::

        name.unit       value : descr

    Arguments:
        line (str): line from a LAS header section
        section_name (str): Name of the section the 'line' is from. The default
        value is None.


    Returns:
        A dictionary with keys 'name', 'unit', 'value', and 'descr', each
        containing a string as value.

    """
    d = {"name": "", "unit": "", "value": "", "descr": ""}

    # Set defaults for local variables.
    patterns = []
    m = None

    if pattern is None:
        patterns = configure_metadata_patterns(line, section_name)
    else:  # pattern was passed in on function call
        patterns.append(pattern)

    for pattern in patterns:
        # Attempt to parse the section line's name(mnemonic), unit, value and
        # descr fields with the given pattern.
        m = re.match(pattern, line)
        if m is not None:
            break

    mdict = m.groupdict()
    for key, value in mdict.items():
        d[key] = value.strip()
        if key == "unit":
            if d[key].endswith("."):
                d[key] = d[key].strip(".")  # see issue #36
    return d


def configure_metadata_patterns(line, section_name):
    """Configure regular-expression patterns to parse section meta-data lines.

    Arguments:
        line (str): line from LAS header section
        section_name (str): Name of the section the 'line' is from.

    Returns:
        An array of regular-expression strings (patterns).
    """

    # Default return value
    patterns = []

    # Default regular expressions for name, value and desc fields
    name_re = r"\.?(?P<name>[^.]*)\."
    value_re = r"(?P<value>.*):"
    desc_re = r"(?P<descr>.*)"

    # Default regular expression for unit field. Note that we
    # attempt to match "1000 psi" as a special case which allows
    # a single whitespace character, in contradiction to the LAS specification
    # See GitHub issue #363 for details.
    unit_re = r"(?P<unit>([0-9]+\s)?[^\s]*)"

    # Alternate regular expressions for special cases
    value_without_colon_delimiter_re = r"(?P<value>[^:]*)"
    value_with_time_colon_re = (
        r"(?P<value>.*?)(?:(?<!( [0-2][0-3]| hh| HH)):(?!([0-5][0-9]|mm|MM)))"
    )
    name_with_dots_re = r"\.?(?P<name>[^.].*[.])\."
    no_desc_re = ""

    # Configure special cases
    # 1. missing colon delimiter and description field
    # 2. double_dots '..' caused by mnemonic abbreviation (with period)
    #    next to the dot delimiter.
    if not ":" in line:
        # If there isn't a colon delimiter then there isn't
        # a description field either.
        value_re = value_without_colon_delimiter_re
        desc_re = no_desc_re

        if ".." in line and section_name == "Curves":
            name_re = name_with_dots_re
    else:
        if ".." in line and section_name == "Curves":
            double_dot = line.find("..")
            desc_colon = line.rfind(":")

            # Check that a double_dot is not in the
            # description string.
            if double_dot < desc_colon:
                name_re = name_with_dots_re

    if section_name == "Parameter":
        # Search for a value entry with a time-value first.
        pattern = name_re + unit_re + value_with_time_colon_re + desc_re
        patterns.append(pattern)

    # Add the regular pattern for all section_names
    # for the Parameter section this will run after time-value pattern
    pattern = name_re + unit_re + value_re + desc_re
    patterns.append(pattern)

    return patterns
