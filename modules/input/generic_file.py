from modules.input import InputModule
from core.bom import HostEvent


class GenericLogFile(InputModule):

    CONFIG = {
        'DEFAULT_LOG_PATH': "/var/log/file.log"
    }

    @classmethod
    def get_events(cls, path=CONFIG['DEFAULT_LOG_PATH']):
        file = open(path, "r")
        events = []

        for line in file:
            event = HostEvent(cls.__name__)
            event.file = path
            event.content = line
            events.append(event)

        file.close()
        return events
