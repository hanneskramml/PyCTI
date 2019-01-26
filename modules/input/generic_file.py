import os
from flask import flash
from modules.input import InputModule
from core.bom import HostEvent


class GenericLogFile(InputModule):

    CONFIG = {
        'DEFAULT_LOG_PATH': "/var/log/",
        'DEFAULT_LOG_FILE': "event.log"
    }

    @classmethod
    def get_events(cls, path=None, file=None):

        if path is None:
            path = cls.CONFIG['DEFAULT_LOG_PATH']

        if file is None:
            file = cls.CONFIG['DEFAULT_LOG_FILE']

        events = []

        try:
            file = open(os.path.join(path, file), "r")

            for line in file:
                event = HostEvent(cls.__name__)
                event.file = path
                event.content = line
                events.append(event)

            file.close()

        except Exception as e:
            flash(e.__class__.__name__, "error")

        return events
