
from text import Text

class TableDataError(Exception):
    pass

class InvalidRowError(TableDataError):
    pass

class InvalidCellError(TableDataError):
    pass

class Table(object):
    def __init__(self, ncols, title=None):
        ''' Optional: Text object -- title of table to be
            printed as a header over the table
        '''
        if title is not None:
            self.title = self._text_or_error(title)
        else:
            self.title = None

        ''' Number of columns in the table '''
        self.ncols = ncols

        ''' List of (bool, [col data]) tuples
            where bool indicates whether it's a 
            header row and data is the column
            contents.  The contents must be
            Text objects.
        '''
        self.rows = []

    def add_header_row(self, values):
        if len(values) != self.ncols:
            raise InvalidRowError
        values = map(self._text_or_error, values)
        self.rows.append((False, values))

    def add_row(self, values):
        if len(values) != self.ncols:
            raise InvalidRowError
        values = map(self._text_or_error, values)
        self.rows.append((False, values))

    def _text_or_error(self, obj):
        if not isinstance(obj, Text):
            raise InvalidCellError
        return obj
         


