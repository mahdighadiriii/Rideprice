class RidePriceException(Exception):
    """Base exception for RidePrice service"""

    pass


class InvalidInputException(RidePriceException):
    """Invalid input data"""

    pass


class ExternalAPIException(RidePriceException):
    """External API error"""

    pass


class CalculationException(RidePriceException):
    """Price calculation error"""

    pass
