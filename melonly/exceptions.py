"""
Exceptions for the Melonly API client.
"""

from typing import Optional, Dict, Any


class MelonlyAPIError(Exception):
    """Base exception for all Melonly API errors."""
    
    def __init__(
        self, 
        message: str, 
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
    
    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class MelonlyBadRequestError(MelonlyAPIError):
    """Raised when the API returns a 400 Bad Request error."""
    pass


class MelonlyUnauthorizedError(MelonlyAPIError):
    """Raised when the API returns a 401 Unauthorized error."""
    pass


class MelonlyNotFoundError(MelonlyAPIError):
    """Raised when the API returns a 404 Not Found error."""
    pass


class MelonlyInternalServerError(MelonlyAPIError):
    """Raised when the API returns a 500 Internal Server Error."""
    pass


class MelonlyRateLimitError(MelonlyAPIError):
    """Raised when the API rate limit is exceeded."""
    
    def __init__(
        self,
        message: str,
        retry_after: Optional[float] = None,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, status_code, response_data)
        self.retry_after = retry_after


class MelonlyConnectionError(MelonlyAPIError):
    """Raised when there's a connection error to the API."""
    pass


class MelonlyTimeoutError(MelonlyAPIError):
    """Raised when a request times out."""
    pass