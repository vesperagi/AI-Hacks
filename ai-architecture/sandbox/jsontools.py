################################################################################
# Imports
################################################################################

import json


################################################################################
# JSON Tools
################################################################################


def to_json(input_dictionary: dict, indent=4) -> bytes:
    """
    Return the JSON representation of a given dictionary.

    Parameters
    ----------
    input_dictionary : dict
        A dictionary to convert to JSON format.

    indent : int, optional
        Number of spaces to indent each level of the JSON object tree.
        Default value is 4.

    Returns
    -------
    bytes
        A JSON-encoded representation of the input dictionary, with UTF-8 encoding.

    Raises
    ------
    TypeError
        If the input is not a dictionary object.
    """
    return json.dumps(input_dictionary, indent=indent, ensure_ascii=False).encode("utf-8")


def pprint(input_dictionary: dict, indent=4):
    """
    Prints a dictionary in a pretty format.

    Parameters
    ----------
    input_dictionary : dict
        Dictionary to be printed.

    indent : int, optional
        Number of spaces to be used for indentation. Default value is 4.

    Returns
    -------
    None
        The function returns nothing, it just prints the input dictionary in a pretty format.
    """
    json_string = to_json(input_dictionary, indent=indent).decode()
    print(json_string)