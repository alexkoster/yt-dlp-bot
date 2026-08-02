import uuid
from typing import Literal

from pydantic import StrictStr

from yt_shared.enums import RabbitPayloadType
from yt_shared.schemas.base_rabbit import BaseRabbitDownloadPayload
from yt_shared.utils.common import format_bytes


class ProgressDownloadPayload(BaseRabbitDownloadPayload):
    """Payload representing download progress status."""

    type: Literal[RabbitPayloadType.PROGRESS] = RabbitPayloadType.PROGRESS
    task_id: uuid.UUID | None = None
    downloaded_bytes: int = 0
    total_bytes: int | None = None
    speed: float | None = None
    eta: int | float | None = None
    status: StrictStr = 'downloading'
    filename: StrictStr | None = None

    @property
    def percent(self) -> float:
        if self.total_bytes and self.total_bytes > 0:
            return round((self.downloaded_bytes / self.total_bytes) * 100, 1)
        return 0.0

    def format_progress_bar(self, length: int = 10) -> str:
        return self.format_ascii_progress_bar(length=length)

    def format_ascii_progress_bar(
        self, length: int = 10, fill_char: str = '█', empty_char: str = '░'
    ) -> str:
        pct = self.percent
        filled = int(round(length * pct / 100))
        bar = fill_char * filled + empty_char * (length - filled)
        return f'[{bar}]'

    def format_emoji_progress_bar(
        self, length: int = 10, filled_emoji: str = '🟩', empty_emoji: str = '⬜'
    ) -> str:
        pct = self.percent
        filled = int(round(length * pct / 100))
        return filled_emoji * filled + empty_emoji * (length - filled)

    def format_speed(self) -> str:
        if self.speed and self.speed > 0:
            return f'{format_bytes(int(self.speed))}/s'
        return 'N/A'

    def format_eta(self) -> str:
        if self.eta is not None and self.eta >= 0:
            total_seconds = int(self.eta)
            mins, secs = divmod(total_seconds, 60)
            hrs, mins = divmod(mins, 60)
            if hrs > 0:
                return f'{hrs:02d}:{mins:02d}:{secs:02d}'
            return f'{mins:02d}:{secs:02d}'
        return 'N/A'

    def format_downloaded(self) -> str:
        return format_bytes(self.downloaded_bytes)

    def format_total(self) -> str:
        if self.total_bytes:
            return format_bytes(self.total_bytes)
        return 'N/A'
