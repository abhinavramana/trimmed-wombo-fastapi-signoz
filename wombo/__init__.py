import logging
import typing
import nest_asyncio # Should not be commented out

"""
***************************************************************************************************
ALERT: THIS FILE SHOULD NEVER CONTAIN ANY WOMBO PACKAGE IMPORTS

This should never be taken out of the basic init because this is the first thing that should
be initialized even before the imports
***************************************************************************************************

These functions do nothing if the root logger already has handlers configured, unless the keyword argument *force*
is set to `True`
"""

logging.info("Initialized the logger...")

nest_asyncio.apply()  # Should not be commented out


def convert_comma_separated_to_set(input_string: str) -> typing.Set[str]:
    list_of_strings = input_string.split(",")
    return set(list_of_strings)
