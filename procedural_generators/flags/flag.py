from PIL.Image import Image

class Flag(object):

    def __init__(self, file_name):
        self.image = Image()
        self.image.resize((128, 256))

        self._file_name = file_name


    def save(self):
        self.image.save(open(self._file_name))