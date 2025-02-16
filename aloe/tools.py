"""
Useful tools for writing Aloe steps.

See also :class:`aloe.world`.
"""

import re
from datetime import datetime


def guess_types(data):
    """
    Converts a record or list of records from strings contained in
    outlines, table or hashes into a version with the types guessed.

    :param data: a :attr:`Scenario.outlines`, :attr:`Step.table`,
        :attr:`Step.hashes` or any other :class:`list`,
        list of lists or list of dicts.

    Will guess the following (in priority order):

     * :class:`bool` (``true``/``false``)
     * :class:`None` (``null``)
     * :class:`int`
     * :class:`date` in ISO format (``yyyy-mm-dd``)
     * :class:`str`

    The function operates recursively, so you should be able to pass nearly
    anything to it. At the very least basic types plus
    :class:`dict` and iterables.
    """

    # convert bytes to strings
    if isinstance(data, bytes):
        data = data.decode()

    if isinstance(data, str):
        if data == "true":
            data = True
        elif data == "false":
            data = False
        elif data == "null":
            data = None
        elif data.isdigit() and not re.match("^0[0-9]+", data):
            data = int(data)
        elif re.match(r"^\d{4}-\d{2}-\d{2}$", data):
            data = datetime.strptime(data, "%Y-%m-%d").date()
        else:
            # it's a string
            pass

        return data

    # if it's a dict, recurse as a dict
    if isinstance(data, dict):
        return {guess_types(key): guess_types(data) for key, data in data.items()}

    # try to recurse as an iterable
    try:
        return [guess_types(val) for val in data]
    except TypeError:
        pass

    #  give up
    return data
