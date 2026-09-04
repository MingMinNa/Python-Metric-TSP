
class IncompleteMatrixError(Exception):
    """
    Raised when the distance matrix contains missing entries.
    """


class TriangleInequalityError(Exception):
    """
    Raised when the triangle inequality is violated.
    """