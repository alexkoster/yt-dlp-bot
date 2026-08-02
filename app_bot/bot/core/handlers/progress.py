from pyrogram.errors import MessageIdInvalid, MessageNotModified
from yt_shared.schemas.progress import ProgressDownloadPayload

from bot.core.handlers.abstract import AbstractDownloadHandler
from bot.core.utils import bold, code


class ProgressDownloadHandler(AbstractDownloadHandler):
    """Handle download progress updates from worker."""

    _body: ProgressDownloadPayload

    async def handle(self) -> None:
        if not (self._body.from_chat_id and self._body.context.ack_message_id):
            return

        text = self._format_progress_text()
        try:
            await self._bot.edit_message_text(
                chat_id=self._body.from_chat_id,
                message_id=self._body.context.ack_message_id,
                text=text,
            )
        except (MessageIdInvalid, MessageNotModified) as err:
            self._log.warning(
                'Could not edit the progress message id "%s": %s',
                self._body.context.ack_message_id,
                err,
            )

    def _format_progress_text(self) -> str:
        pct = self._body.percent
        emoji_bar = self._body.format_emoji_progress_bar()
        downloaded = self._body.format_downloaded()
        total = self._body.format_total()
        speed = self._body.format_speed()
        eta = self._body.format_eta()

        return (
            f'⏬ {bold(f"Downloading: {pct}%")}\n'
            f'{emoji_bar}\n'
            f'📦 {bold("Downloaded:")} {downloaded} / {total}\n'
            f'⚡ {bold("Speed:")} {speed} | ⏳ {bold("ETA:")} {eta}'
        )
