"""
XReason SDK Exceptions
"""


class XReasonError(Exception):
    """Base exception for XReason SDK."""
    pass


class XReasonAPIError(XReasonError):
    """Exception raised for API-related errors."""
    
    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class XReasonValidationError(XReasonError):
    """Exception raised for validation errors."""
    pass


class XReasonConnectionError(XReasonError):
    """Exception raised for connection errors."""
    pass


class XReasonTimeoutError(XReasonError):
    """Exception raised for timeout errors."""
    pass


class XReasonAuthenticationError(XReasonAPIError):
    """Exception raised for authentication errors."""
    pass


class XReasonRateLimitError(XReasonAPIError):
    """Exception raised for rate limit errors."""
    pass
