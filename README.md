# Melonly API Python Client

A comprehensive Python client library for the Melonly API, providing easy access to server management, applications, logs, shifts, and more.

## Features

- **Full API Coverage**: Complete support for all Melonly API endpoints
- **Type Hints**: Full type annotations for better IDE support and code safety
- **Async Support**: Both synchronous and asynchronous client implementations
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Pagination**: Built-in pagination support for list endpoints
- **Rate Limiting**: Automatic rate limiting and retry logic
- **Documentation**: Extensive documentation and examples

## Installation

```bash
pip install melonly-api
```

## Quick Start

```python
from melonly import MelonlyClient

# Initialize the client
client = MelonlyClient(token="your-api-token")

# Get server information
server = client.get_server_info()
print(f"Server: {server.name}")

# Get applications
applications = client.get_applications()
for app in applications.data:
    print(f"Application: {app.title}")

# Get logs with pagination
logs = client.get_logs(page=1, limit=50)
for log in logs.data:
    print(f"Log: {log.text}")
```

## Async Usage

```python
import asyncio
from melonly import AsyncMelonlyClient

async def main():
    client = AsyncMelonlyClient(token="your-api-token")
    
    # Get server information
    server = await client.get_server_info()
    print(f"Server: {server.name}")
    
    # Don't forget to close the client
    await client.close()

# Run the async function
asyncio.run(main())
```

## API Reference

### Applications

```python
# Get all applications
applications = client.get_applications()

# Get specific application
app = client.get_application("app_id")

# Get application responses
responses = client.get_application_responses("app_id")

# Get user application responses
user_responses = client.get_user_application_responses("user_id")
```

### Members

```python
# Get all members
members = client.get_members()

# Get specific member
member = client.get_member("member_id")

# Get member by Discord ID
member = client.get_member_by_discord_id("discord_id")
```

### Logs

```python
# Get all logs
logs = client.get_logs()

# Get specific log
log = client.get_log("log_id")

# Get logs by user
user_logs = client.get_user_logs("username")

# Get logs by staff
staff_logs = client.get_staff_logs("staff_id")
```

### Shifts

```python
# Get all shifts
shifts = client.get_shifts()

# Get specific shift
shift = client.get_shift("shift_id")
```

### Other Resources

```python
# Get roles
roles = client.get_roles()
role = client.get_role("role_id")

# Get LOAs (Leave of Absence)
loas = client.get_loas()
loa = client.get_loa("loa_id")
user_loas = client.get_user_loas("member_id")

# Get join requests
join_requests = client.get_join_requests()
join_request = client.get_join_request("user_id")

# Get audit logs
audit_logs = client.get_audit_logs()
```

## Error Handling

```python
from melonly import MelonlyClient, MelonlyAPIError, MelonlyNotFoundError

client = MelonlyClient(token="your-token")

try:
    member = client.get_member("invalid_id")
except MelonlyNotFoundError:
    print("Member not found")
except MelonlyAPIError as e:
    print(f"API Error: {e.message}")
```

## Configuration

The client can be configured with various options:

```python
client = MelonlyClient(
    token="your-token",
    base_url="https://api.melonly.xyz/api/v1",  # Custom base URL
    timeout=30,  # Request timeout in seconds
    max_retries=3,  # Maximum number of retries
    retry_delay=1.0,  # Delay between retries
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: [https://melonly-api.readthedocs.io/](https://melonly-api.readthedocs.io/)
- Issues: [https://github.com/yourusername/melonly-api/issues](https://github.com/yourusername/melonly-api/issues)
- Melonly API Documentation: [https://api.melonly.xyz/docs](https://api.melonly.xyz/docs)