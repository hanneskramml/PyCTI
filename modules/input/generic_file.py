import traceback
from flask import flash

from modules.input import InputModule
from core.bom import GenericEvent


class GenericLogFile(InputModule):

    CONFIG = {
        'ALLOWED_EXTENSIONS': {'log', 'txt'}
    }

    @classmethod
    def get_events(cls, file=None):

        if file is None:
            return []

        if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() not in cls.CONFIG.get("ALLOWED_EXTENSIONS"):
            flash("Allowed file extensions: {}".format(cls.CONFIG.get("ALLOWED_EXTENSIONS")), "error")
            return []

        events = []
        try:
            for line in file:
                if len(line.strip()) == 0:
                    continue

                event = GenericEvent(cls.__name__)
                event.content = line
                events.append(event)

            file.close()

        except Exception:
            flash(traceback.format_exc(0), "error")

        return events
