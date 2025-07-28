"""
Synchronous client for the Melonly API.
"""

import time
from typing import Optional, Dict, Any, List, Union
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import (
    MelonlyAPIError,
    MelonlyBadRequestError,
    MelonlyUnauthorizedError,
    MelonlyNotFoundError,
    MelonlyInternalServerError,
    MelonlyRateLimitError,
    MelonlyConnectionError,
    MelonlyTimeoutError,
)
from .models import (
    Application,
    ApplicationResponse,
    AuditLogEvent,
    JoinRequest,
    LOA,
    Log,
    Member,
    Role,
    Server,
    Shift,
    PaginatedResponse,
)


class MelonlyClient:
    """Synchronous client for the Melonly API."""

    def __init__(
        self,
        token: str,
        base_url: str = "https://api.melonly.xyz/api/v1",
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """
        Initialize the Melonly API client.

        Args:
            token: API authentication token
            base_url: Base URL for the API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            retry_delay: Delay between retry attempts in seconds
        """
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Setup session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=retry_delay,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set default headers
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "melonly-api-python/1.0.0",
        })

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            params: Query parameters
            json_data: JSON request body

        Returns:
            JSON response data

        Raises:
            MelonlyAPIError: For various API errors
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=self.timeout,
            )
            
            # Handle rate limiting with retry-after
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    try:
                        retry_after_seconds = float(retry_after)
                        time.sleep(retry_after_seconds)
                        # Retry the request once after waiting
                        response = self.session.request(
                            method=method,
                            url=url,
                            params=params,
                            json=json_data,
                            timeout=self.timeout,
                        )
                    except ValueError:
                        pass
            
            # Parse response JSON
            try:
                response_data = response.json()
            except ValueError:
                response_data = {}

            # Handle different status codes
            if response.status_code == 200:
                return response_data
            elif response.status_code == 400:
                error_msg = response_data.get("error", "Bad request")
                raise MelonlyBadRequestError(error_msg, 400, response_data)
            elif response.status_code == 401:
                error_msg = response_data.get("error", "Unauthorized")
                raise MelonlyUnauthorizedError(error_msg, 401, response_data)
            elif response.status_code == 404:
                error_msg = response_data.get("error", "Not found")
                raise MelonlyNotFoundError(error_msg, 404, response_data)
            elif response.status_code == 429:
                error_msg = response_data.get("error", "Rate limit exceeded")
                retry_after = response.headers.get("Retry-After")
                raise MelonlyRateLimitError(
                    error_msg, 
                    float(retry_after) if retry_after else None,
                    429, 
                    response_data
                )
            elif response.status_code >= 500:
                error_msg = response_data.get("error", "Internal server error")
                raise MelonlyInternalServerError(error_msg, response.status_code, response_data)
            else:
                error_msg = f"HTTP {response.status_code}: {response.reason}"
                raise MelonlyAPIError(error_msg, response.status_code, response_data)

        except requests.exceptions.Timeout:
            raise MelonlyTimeoutError("Request timed out")
        except requests.exceptions.ConnectionError:
            raise MelonlyConnectionError("Failed to connect to API")
        except requests.exceptions.RequestException as e:
            raise MelonlyAPIError(f"Request failed: {str(e)}")

    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()

    # Server Information
    def get_server_info(self) -> Server:
        """Get server information."""
        data = self._make_request("GET", "/server/info")
        return Server.from_dict(data)

    # Applications
    def get_applications(
        self, page: int = 1, limit: int = 10
    ) -> PaginatedResponse[Application]:
        """Get paginated list of applications."""
        params = {"page": page, "limit": limit}
        data = self._make_request("GET", "/server/applications", params=params)
        applications = [Application.from_dict(item) for item in data["data"]]
        return PaginatedResponse(
            data=applications,
            page=data["page"],
            page_size=data["pageSize"],
            total=data["total"],
            total_pages=data["totalPages"],
        )

    def get_application(self, application_id: str) -> Application:
        """Get a specific application by ID."""
        data = self._make_request("GET", f"/server/applications/{application_id}")
        return Application.from_dict(data)

    def get_application_responses(
        self, application_id: str, page: int = 1, limit: int = 10
    ) -> PaginatedResponse[ApplicationResponse]:
        """Get responses for a specific application."""
        params = {"page": page, "limit": limit}
        data = self._make_request(
            "GET", f"/server/applications/{application_id}/responses", params=params
        )
        responses = [ApplicationResponse.from_dict(item) for item in data["data"]]
        return PaginatedResponse(
            data=responses,
            page=data["page"],
            page_size=data["pageSize"],
            total=data["total"],
            total_pages=data["totalPages"],
        )

    def get_user_application_responses(
        self, user_id: str, page: int = 1, limit: int = 10
    ) -> PaginatedResponse[ApplicationResponse]:
        """Get application responses for a specific user."""
        params = {"page": page, "limit": limit}
        data = self._make_request(
            "GET", f"/server/applications/user/{user_id}/responses", params=params
        )
        responses = [ApplicationResponse.from_dict(item) for item in data["data"]]
        return PaginatedResponse(
            data=responses,
            page=data["page"],
            page_size=data["pageSize"],
            total=data["total"],
            total_pages=data["totalPages"],
        )

    # Members
    def get_members(
        self, page: int = 1, limit: int = 10
    ) -> PaginatedResponse[Member]:
        """Get paginated list of server members."""
        params = {"page": page, "limit": limit}
        data = self._make_request("GET", "/server/members", params=params)
        members = [Member.from_dict(item) for item in data["data"]]
        return PaginatedResponse(
            data=members,
            page=data["page"],
            page_size=data["pageSize"],
            total=data["total"],
            total_pages=data["totalPages"],
        )

    def get_member(self, member_id: str) -> Member:
        """Get a specific member by ID."""
        data = self._make_request("GET", f"/server/members/{member_id}")
        return Member.from_dict(data)

    def get_member_by_discord_id(self, discord_id: str) -> Member:
        """Get a specific member by Discord ID."""
        data = self._make_request("GET", f"/server/members/discord/{discord_id}")
        return Member.from_dict(data)

    # Logs
    def get_logs(self, page: int = 1, limit: int = 10) -> PaginatedResponse[Log]:
        """Get paginated list of logs."""
        params = {"page": page, "limit": limit}
        data = self._make_request("GET", "/server/logs", params=params)
        logs = [Log.from_dict(item) for item in data["data"]]
        return PaginatedResponse(
            data=logs,
            page=data["page"],
            page_size=data["pageSize"],
            total=data["total"],
            total_pages=data["totalPages"],
        )

    def get_log(self, log_id: str) -> Log:
        """Get a specific log by ID."""
        data = self._make_request("GET", f"/server/logs/{log_id}")
        return Log.from_dict(data)

    def get_user_logs(
        self, username: str, page: int = 1, limit: int = 10
    ) -> PaginatedResponse[Log]:
        """Get logs for a specific user."""
        params = {"page": page, "limit": limit}
        data = self._make_request("GET", f"/server/logs/user/{username}", params=params)
        logs = [Log.from_dict(item) for item in data["data"]]
        return PaginatedResponse(
            data=logs,
            page=data["page"],
            page_size=data["pageSize"],
            total=data["total"],
            total_pages=data["totalPages"],
        )

    def get_staff_logs(
        self, staff_id: str, page: int = 1, limit: int = 10
    ) -> PaginatedResponse[Log]:
        """Get logs created by a specific staff member."""
        params = {"page": page, "limit": limit}
        data = self._make_request("GET", f"/server/logs/staff/{staff_id}", params=params)
        logs = [Log.from_dict(item) for item in data["data"]]
        return PaginatedResponse(
            data=logs,
            page=data["page"],
            page_size=data["pageSize"],
            total=data["total"],
            total_pages=data["totalPages"],
        )

    # Roles
    def get_roles(self, page: int = 1, limit: int = 10) -> PaginatedResponse[Role]:
        """Get paginated list of roles."""
        params = {"page": page, "limit": limit}
        data = self._make_request("GET", "/server/roles", params=params)
        roles = [Role.from_dict(item) for item in data["data"]]
        return PaginatedResponse(
            data=roles,
            page=data["page"],
            page_size=data["pageSize"],
            total=data["total"],
            total_pages=data["totalPages"],
        )

    def get_role(self, role_id: str) -> Role:
        """Get a specific role by ID."""
        data = self._make_request("GET", f"/server/roles/{role_id}")
        return Role.from_dict(data)

    # Shifts
    def get_shifts(self, page: int = 1, limit: int = 10) -> PaginatedResponse[Shift]:
        """Get paginated list of shifts."""
        params = {"page": page, "limit": limit}
        data = self._make_request("GET", "/server/shifts", params=params)
        shifts = [Shift.from_dict(item) for item in data["data"]]
        return PaginatedResponse(
            data=shifts,
            page=data["page"],
            page_size=data["pageSize"],
            total=data["total"],
            total_pages=data["totalPages"],
        )

    def get_shift(self, shift_id: str) -> Shift:
        """Get a specific shift by ID."""
        data = self._make_request("GET", f"/server/shifts/{shift_id}")
        return Shift.from_dict(data)

    # LOAs (Leave of Absence)
    def get_loas(self, page: int = 1, limit: int = 10) -> PaginatedResponse[LOA]:
        """Get paginated list of LOAs."""
        params = {"page": page, "limit": limit}
        data = self._make_request("GET", "/server/loas", params=params)
        loas = [LOA.from_dict(item) for item in data["data"]]
        return PaginatedResponse(
            data=loas,
            page=data["page"],
            page_size=data["pageSize"],
            total=data["total"],
            total_pages=data["totalPages"],
        )

    def get_loa(self, loa_id: str) -> LOA:
        """Get a specific LOA by ID."""
        data = self._make_request("GET", f"/server/loas/{loa_id}")
        return LOA.from_dict(data)

    def get_user_loas(
        self, member_id: str, page: int = 1, limit: int = 10
    ) -> PaginatedResponse[LOA]:
        """Get LOAs for a specific user."""
        params = {"page": page, "limit": limit}
        data = self._make_request("GET", f"/server/loas/user/{member_id}", params=params)
        loas = [LOA.from_dict(item) for item in data["data"]]
        return PaginatedResponse(
            data=loas,
            page=data["page"],
            page_size=data["pageSize"],
            total=data["total"],
            total_pages=data["totalPages"],
        )

    # Join Requests
    def get_join_requests(
        self, page: int = 1, limit: int = 10
    ) -> PaginatedResponse[JoinRequest]:
        """Get paginated list of join requests."""
        params = {"page": page, "limit": limit}
        data = self._make_request("GET", "/server/join-requests", params=params)
        join_requests = [JoinRequest.from_dict(item) for item in data["data"]]
        return PaginatedResponse(
            data=join_requests,
            page=data["page"],
            page_size=data["pageSize"],
            total=data["total"],
            total_pages=data["totalPages"],
        )

    def get_join_request(self, user_id: str) -> JoinRequest:
        """Get a specific join request by user ID."""
        data = self._make_request("GET", f"/server/join-requests/{user_id}")
        return JoinRequest.from_dict(data)

    # Audit Logs
    def get_audit_logs(
        self, page: int = 1, limit: int = 10
    ) -> PaginatedResponse[AuditLogEvent]:
        """Get paginated list of audit logs."""
        params = {"page": page, "limit": limit}
        data = self._make_request("GET", "/server/audit-logs", params=params)
        audit_logs = [AuditLogEvent.from_dict(item) for item in data["data"]]
        return PaginatedResponse(
            data=audit_logs,
            page=data["page"],
            page_size=data["pageSize"],
            total=data["total"],
            total_pages=data["totalPages"],
        )

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()