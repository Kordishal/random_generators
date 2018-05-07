

class NameTemplate(object):
    """A name template.

    :param content:     The content of the template. Determines how names from different lists are combined when
                        generating a new name.
    :param name:        A name for this template (optional, default: '')
    :param tags:        Tags for the template. These are uses to specify which list tags this template will choose.
    :param weight:      The weight will determine how likely this template is to be chosen when several templates can
                        be selected.
    """

    def __init__(self, content: str, name='', tags=list(), weight=10):
        self.content = content
        self.name = name
        self.tags = tags
        self.weight = weight


