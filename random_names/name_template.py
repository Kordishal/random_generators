from random_names.exceptions import UnknownNameList
import re


class NameTemplate(object):
    """A name template.

    :param content:     The content of the template. Determines how names from different lists are combined when
                        generating a new name.
    :param name:        A name for this template (optional, default: '')
    :param tags:        Tags for the template. These are uses to specify which list tags this template will choose.
    :param weight:      The weight will determine how likely this template is to be chosen when several templates can
                        be selected.
    """

    def __init__(self, name: str, content: str, tags: list, weight: int):
        self.name = name
        self.content = content
        self.tags = tags
        self.weight = weight

    def expand(self, name_sets):
        result = self.content
        matches = re.findall('<.*?>', result)
        for match in matches:
            temp = match.strip('<>')
            nameset_id, namelist_id = temp.split(':')
            try:
                name = name_sets[nameset_id].name_lists[namelist_id].get_name()
            except KeyError:
                raise UnknownNameList('The name list with tag {} could not be found!'.format(namelist_id))
            result = re.sub(match, name, result)
        return result




