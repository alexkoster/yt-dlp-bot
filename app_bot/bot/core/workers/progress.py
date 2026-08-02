from yt_shared.rabbit.rabbit_config import PROGRESS_QUEUE
from yt_shared.schemas.progress import ProgressDownloadPayload
from yt_shared.utils.tasks.tasks import create_task

from bot.core.handlers.progress import ProgressDownloadHandler
from bot.core.workers.abstract import AbstractDownloadResultWorker, RabbitWorkerType


class ProgressDownloadResultWorker(AbstractDownloadResultWorker):
    TYPE = RabbitWorkerType.PROGRESS
    QUEUE_TYPE = PROGRESS_QUEUE
    SCHEMA_CLS = (ProgressDownloadPayload,)
    HANDLER_CLS = ProgressDownloadHandler

    async def _process_body(self, body: ProgressDownloadPayload) -> None:
        self._spawn_handler_task(body)

    def _spawn_handler_task(self, body: ProgressDownloadPayload) -> None:
        task_name = self.HANDLER_CLS.__class__.__name__
        create_task(
            self.HANDLER_CLS(body=body, bot=self._bot).handle(),
            task_name=task_name,
            logger=self._log,
            exception_message='Task "%s" raised an exception',
            exception_message_args=(task_name,),
        )
