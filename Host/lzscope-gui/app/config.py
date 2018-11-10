# -*- coding: utf-8 -*-
"""Configuration mechanisms.

Stolen from Flask,
https://github.com/mitsuhiko/flask/blob/0.10-maintenance/flask/config.py
"""



def from_object(obj=None, verbose=False):
    """Imports all upper-cased variables from an object.

    Input:
        obj:
            An object or a name of the one to import variables.
        verbose (bool):
            Print a list of the imported variables (default is ``False``).
    """

    if not obj:
        raise ValueError(u"Object 'obj' or its name undefined.")

    # Import the object by its name if it's given.
    if isinstance(obj, str):
        obj = __import__(obj)

    if verbose:
        print(u"Import variables from '{:s}':".format(obj.__name__))

    for key in dir(obj):
        if key.isupper():
            globals()[key] = getattr(obj, key)

            if verbose:
                value = globals()[key]
                if type(value) is str:
                    print("\t{}: '{}'".format(key, value))
                else:
                    print("\t{}: {}".format(key, value))
