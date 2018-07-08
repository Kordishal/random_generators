from random_names.exceptions import MissingIdError
import json


def read_name_set_file(file_name: str) -> dict:
    """

    :param file_name:   The file name to be read (incl. path!)
    :return:            A dictionary of the name set.
    :raises MissingIdError:         When the given name set does not have an id.
    :raises MissingNameListError:   When the given name set does not have a single name list.
    """
    with open(file_name, 'r') as f:
        content = f.read()
        name_set = json.loads(content)

        if 'id' not in name_set:
            raise MissingIdError('The name set in {} has no id.'.format(file_name))

        return name_set
