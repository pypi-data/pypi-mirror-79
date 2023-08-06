import json
import logging


def get_local_json_file_as_dict(path_to_file):
    """
    Converts a local JSON file into a dict
    Args:
        path_to_file (string): path to local JSON file
    Returns:
        file_contents (dict): dict representation of JSON file
    """

    try:
        local_file = open(path_to_file, 'r')
        file_string_contents = local_file.read()
        file_contents = json.loads(file_string_contents)
    except Exception as e:
        logging.exception(e)
        file_contents = {}

    return file_contents
