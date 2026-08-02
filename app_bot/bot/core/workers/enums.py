from enum import StrEnum


class RabbitWorkerType(StrEnum):
    ERROR = 'ERROR'
    PROGRESS = 'PROGRESS'
    SUCCESS = 'SUCCESS'
