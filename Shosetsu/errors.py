class Error(Exception):
    pass

class VNDBOneResult(Error):
    """
    This exception is raised when we search for an item but only get on result so VNDB passes us directly to that content.

    Attributes:
            expression - The input name that returned only one result
            vnid - The ID of this result
    """
    def __init__(self, expression, vnid):
        self.expression = expression
        self.vnid = vnid

    def __str__(self):
        return "Search {} only had one result at ID {}.".format(self.expression, self.vnid)

    def __repr__(self):
        return "Search {} only had one result at ID {}.".format(self.expression, self.vnid)

class VNDBNoResults(Error):
    """
    This exception is raised when we search for content but find no results

    Attributes:
            expression - The input name that returned no results
    """
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return "Search {} has no results.".format(self.expression)

    def __repr__(self):
        return "Search {} has no results.".format(self.expression)

class VNDBBadStype(Error):
    """
    This exception is raised when a bad search type is passed

    Attributes:
            expression - The input name that returned only one result
    """
    def __init__(self, expression, vnid):
        self.expression = expression

    def __str__(self):
        return "{} is not a valid search type.".format(self.expression)

    def __repr__(self):
        return "{} is not a valid search type.".format(self.expression)