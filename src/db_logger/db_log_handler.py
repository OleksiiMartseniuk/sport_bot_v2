import logging

from src.database.base import sync_session
from src.database.models.logger import StatusLog
from src.utils.utils import LogLevel


db_default_formatter = logging.Formatter()


class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        trace = None

        if record.exc_info:
            trace = db_default_formatter.formatException(record.exc_info)
        msg = record.getMessage()

        kwargs = {
            'logger_name': record.name,
            'level': LogLevel(record.levelno),
            'msg': msg,
            'trace': trace
        }

        with sync_session() as session:
            session.add(StatusLog(**kwargs))
            session.commit()
