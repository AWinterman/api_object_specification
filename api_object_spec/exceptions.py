class ParsimoniousError(Exception):
    def __init__(self, exception):
        """
        A class for wrapping parsimonious errors to make them a bit more sensible to users of this library.

        :param exception: The original parsimonious exception
        :return: self
        """

        self.exception = exception

    def __unicode__(self):
        return u'Encountered an error parsing your api specification. The error was: \n {}'.format(self.exception)

    def __str__(self):
        return str(unicode(self))