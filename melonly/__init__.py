"""
Melonly API Python Client

A comprehensive Python client library for the Melonly API.
"""

from .client import MelonlyClient
from .async_client import AsyncMelonlyClient
from .exceptions import (
    MelonlyAPIError,
    MelonlyBadRequestError,
    MelonlyUnauthorizedError,
    MelonlyNotFoundError,
    MelonlyInternalServerError,
    MelonlyRateLimitError,
)
from .models import *

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

__all__ = [
    # Clients
    "MelonlyClient",
    "AsyncMelonlyClient",
    # Exceptions
    "MelonlyAPIError",
    "MelonlyBadRequestError", 
    "MelonlyUnauthorizedError",
    "MelonlyNotFoundError",
    "MelonlyInternalServerError",
    "MelonlyRateLimitError",
    # Models (imported from models.__all__)
    "Application",
    "ApplicationResponse", 
    "AuditLogEvent",
    "JoinRequest",
    "LOA",
    "Log",
    "Member",
    "Role",
    "Server",
    "Shift",
    "PaginatedResponse",
]