from random_names.exceptions import NameListMissingError
import json


def read_name_set_file(file_name: str) -> dict:
    """

    :param file_name:   The file name to be read (incl. path!)
    :return:            A dictionary of the name set.
    """
    with open(file_name, 'r', encoding='utf-8-sig') as file:
        content = file.read()
        name_set = json.loads(content)

        if 'name_list' not in name_set:
            raise NameListMissingError('The name set in {} has no name lists.'.format(file_name))
        return name_set


def check_name_set(name_set_dict: dict):
    pass
