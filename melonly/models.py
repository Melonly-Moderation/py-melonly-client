"""
Data models for the Melonly API.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, TypeVar, Generic
from datetime import datetime

T = TypeVar('T')


@dataclass
class PaginatedResponse(Generic[T]):
    """Generic paginated response wrapper."""
    data: List[T]
    page: int
    page_size: int
    total: int
    total_pages: int


@dataclass 
class Application:
    """Represents an application."""
    id: str
    title: str
    description: str
    server_id: str
    created_at: int
    last_updated: int
    accepting_responses: bool
    questions: Dict[str, Any]
    sections: List[Dict[str, Any]]
    presets: List[Dict[str, Any]]
    color: str
    banner_key: str
    submission_message: str
    closed_message: str
    cooldown: int
    approval_roles: List[str]
    denial_roles: List[str]
    acceptance_remove_roles: List[str]
    denial_remove_roles: List[str]
    reviewer_roles: List[str]
    review_only_roles: List[str]
    required_discord_roles: List[str]
    blocked_discord_roles: List[str]
    submit_mention_roles: List[str]
    results_channel_id: str
    events_channel_id: str
    results_mention_user: bool
    reveal_reviewer: bool
    require_discord_member: bool
    require_approved_reason: bool
    required_denial_reason: bool
    collect_roblox_account: bool
    roblox_group_id: str
    guild_member_age: int
    invite_on_approval: bool
    stage_responses: bool
    max_logs: int
    ban_appeal: int
    ban_appeal_note: bool
    appeal_cooldown: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Application':
        """Create an Application instance from API response data."""
        return cls(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            server_id=data['serverId'],
            created_at=data['createdAt'],
            last_updated=data['lastUpdated'],
            accepting_responses=data['acceptingResponses'],
            questions=data['questions'],
            sections=data['sections'],
            presets=data['presets'],
            color=data['color'],
            banner_key=data['bannerKey'],
            submission_message=data['submissionMessage'],
            closed_message=data['closedMessage'],
            cooldown=data['cooldown'],
            approval_roles=data['approvalRoles'],
            denial_roles=data['denialRoles'],
            acceptance_remove_roles=data['acceptanceRemoveRoles'],
            denial_remove_roles=data['denialRemoveRoles'],
            reviewer_roles=data['reviewerRoles'],
            review_only_roles=data['reviewOnlyRoles'],
            required_discord_roles=data['requiredDiscordRoles'],
            blocked_discord_roles=data['blockedDiscordRoles'],
            submit_mention_roles=data['submitMentionRoles'],
            results_channel_id=data['resultsChannelId'],
            events_channel_id=data['eventsChannelId'],
            results_mention_user=data['resultsMentionUser'],
            reveal_reviewer=data['revealReviewer'],
            require_discord_member=data['requireDiscordMember'],
            require_approved_reason=data['requireApprovedReason'],
            required_denial_reason=data['requiredDenialReason'],
            collect_roblox_account=data['collectRobloxAccount'],
            roblox_group_id=data['robloxGroupId'],
            guild_member_age=data['guildMemberAge'],
            invite_on_approval=data['inviteOnApproval'],
            stage_responses=data['stageResponses'],
            max_logs=data['maxLogs'],
            ban_appeal=data['banAppeal'],
            ban_appeal_note=data['banAppealNote'],
            appeal_cooldown=data['appealCooldown'],
        )


@dataclass
class ApplicationResponse:
    """Represents an application response."""
    id: str
    application_id: str
    user_id: str
    roblox_id: str
    answers: Dict[str, Any]
    comments: Dict[str, Any]
    flagged: Dict[str, Any]
    status: int
    staging_status: int
    reason: str
    created_at: int
    reviewed_at: int
    reviewed_by: str
    finalized_at: int
    finalized_by: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ApplicationResponse':
        """Create an ApplicationResponse instance from API response data."""
        return cls(
            id=data['id'],
            application_id=data['applicationId'],
            user_id=data['userId'],
            roblox_id=data['robloxId'],
            answers=data['answers'],
            comments=data['comments'],
            flagged=data['flagged'],
            status=data['status'],
            staging_status=data['stagingStatus'],
            reason=data['reason'],
            created_at=data['createdAt'],
            reviewed_at=data['reviewedAt'],
            reviewed_by=data['reviewedBy'],
            finalized_at=data['finalizedAt'],
            finalized_by=data['finalizedBy'],
        )


@dataclass
class AuditLogEvent:
    """Represents an audit log event."""
    id: str
    server_id: str
    application_id: str
    user_id: str
    type: int
    description: Dict[str, Any]
    timestamp: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AuditLogEvent':
        """Create an AuditLogEvent instance from API response data."""
        return cls(
            id=data['id'],
            server_id=data['serverId'],
            application_id=data['applicationId'],
            user_id=data['userId'],
            type=data['type'],
            description=data['description'],
            timestamp=data['timestamp'],
        )


@dataclass
class JoinRequest:
    """Represents a join request."""
    user_id: str
    server_id: str
    join_code: str
    created_at: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JoinRequest':
        """Create a JoinRequest instance from API response data."""
        return cls(
            user_id=data['userId'],
            server_id=data['serverId'],
            join_code=data['joinCode'],
            created_at=data['createdAt'],
        )


@dataclass
class LOA:
    """Represents a Leave of Absence."""
    id: str
    server_id: str
    member_id: str
    reason: str
    reason_history: List[Dict[str, Any]]
    start_at: int
    end_at: int
    start_type: int
    status: int
    created_at: int
    started_at: int
    ended_at: int
    ended_by: str
    expired_at: int
    reviewed_at: int
    reviewed_by: str
    cancelled_at: int
    deny_reason: str
    extension_requests: List[Dict[str, Any]]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LOA':
        """Create a LOA instance from API response data."""
        return cls(
            id=data['id'],
            server_id=data['serverId'],
            member_id=data['memberId'],
            reason=data['reason'],
            reason_history=data['reasonHistory'],
            start_at=data['startAt'],
            end_at=data['endAt'],
            start_type=data['startType'],
            status=data['status'],
            created_at=data['createdAt'],
            started_at=data['startedAt'],
            ended_at=data['endedAt'],
            ended_by=data['endedBy'],
            expired_at=data['expiredAt'],
            reviewed_at=data['reviewedAt'],
            reviewed_by=data['reviewedBy'],
            cancelled_at=data['cancelledAt'],
            deny_reason=data['denyReason'],
            extension_requests=data['extensionRequests'],
        )


@dataclass
class Log:
    """Represents a log entry."""
    id: str
    server_id: str
    type: int
    type_id: str
    username: str
    roblox_id: str
    text: str
    description: str
    proof: List[Dict[str, Any]]
    created_at: int
    created_by: str
    completed_by: str
    edited_by: List[Dict[str, Any]]
    temp_ban: bool
    unban_at: int
    expired: bool
    expired_at: int
    expired_by: str
    hidden: bool
    hidden_by: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Log':
        """Create a Log instance from API response data."""
        return cls(
            id=data['id'],
            server_id=data['serverId'],
            type=data['type'],
            type_id=data['typeId'],
            username=data['username'],
            roblox_id=data['robloxId'],
            text=data['text'],
            description=data['description'],
            proof=data['proof'],
            created_at=data['createdAt'],
            created_by=data['createdBy'],
            completed_by=data['completedBy'],
            edited_by=data['editedBy'],
            temp_ban=data['tempBan'],
            unban_at=data['unbanAt'],
            expired=data['expired'],
            expired_at=data['expiredAt'],
            expired_by=data['expiredBy'],
            hidden=data['hidden'],
            hidden_by=data['hiddenBy'],
        )


@dataclass
class Member:
    """Represents a server member."""
    id: str
    server_id: str
    roles: List[str]
    created_at: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Member':
        """Create a Member instance from API response data."""
        return cls(
            id=data['id'],
            server_id=data['serverId'],
            roles=data['roles'],
            created_at=data['createdAt'],
        )


@dataclass
class Role:
    """Represents a server role."""
    id: str
    server_id: str
    name: str
    colour: str
    permissions: str
    extra_permissions: int
    linked_discord_role_id: str
    created_at: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Role':
        """Create a Role instance from API response data."""
        return cls(
            id=data['id'],
            server_id=data['serverId'],
            name=data['name'],
            colour=data['colour'],
            permissions=data['permissions'],
            extra_permissions=data['extraPermissions'],
            linked_discord_role_id=data['linkedDiscordRoleId'],
            created_at=data['createdAt'],
        )


@dataclass
class Server:
    """Represents a server."""
    id: str
    name: str
    owner_id: str
    discord_guild_id: str
    join_code: str
    roles: List[Dict[str, Any]]
    created_at: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Server':
        """Create a Server instance from API response data."""
        return cls(
            id=data['id'],
            name=data['name'],
            owner_id=data['ownerId'],
            discord_guild_id=data['discordGuildId'],
            join_code=data['joinCode'],
            roles=data['roles'],
            created_at=data['createdAt'],
        )


@dataclass
class Shift:
    """Represents a shift."""
    id: str
    server_id: str
    member_id: str
    type: str
    wave: int
    auto_end: bool
    break_timestamps: List[Dict[str, Any]]
    created_at: int
    ended_at: int
    ended_by: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Shift':
        """Create a Shift instance from API response data."""
        return cls(
            id=data['id'],
            server_id=data['serverId'],
            member_id=data['memberId'],
            type=data['type'],
            wave=data['wave'],
            auto_end=data['autoEnd'],
            break_timestamps=data['breakTimestamps'],
            created_at=data['createdAt'],
            ended_at=data['endedAt'],
            ended_by=data['endedBy'],
        )


# Export all models
__all__ = [
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