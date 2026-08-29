import uuid
from typing import Literal

from yt_shared.enums import RabbitPayloadType
from yt_shared.schemas.base_rabbit import BaseRabbitDownloadPayload


class ProgressPayload(BaseRabbitDownloadPayload):
    """Payload with download progress context."""

    type: Literal[RabbitPayloadType.PROGRESS] = RabbitPayloadType.PROGRESS
    task_id: uuid.UUID
    message: str
