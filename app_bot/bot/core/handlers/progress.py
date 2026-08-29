import logging
from typing import TYPE_CHECKING

from pyrogram.errors import MessageNotModified
from yt_shared.schemas.progress import ProgressPayload

if TYPE_CHECKING:
    from bot.bot.client import VideoBotClient

class ProgressDownloadHandler:
    def __init__(self, body: ProgressPayload, bot: 'VideoBotClient') -> None:
        self._log = logging.getLogger(self.__class__.__name__)
        self._body = body
        self._bot = bot

    async def handle(self) -> None:
        if not self._body.message_id or not self._body.from_chat_id:
            return

        try:
            await self._bot.edit_message_text(
                chat_id=self._body.from_chat_id,
                message_id=self._body.message_id,
                text=self._body.message,
            )
        except MessageNotModified:
            pass
        except Exception as e:
            self._log.warning('Failed to edit progress message: %s', e)
