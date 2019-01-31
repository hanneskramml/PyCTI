import clamd, traceback
from flask import flash

from core.bom import HostEvent
from modules.input import InputModule


class ClamAV(InputModule):

    CONFIG = {
        'MODULE_NAME': "ClamAV",
        'DEFAULT_ON_ACCESS_SCAN_LOG': "/var/log/clamav/infected.log",
        'DEFAULT_SCAN_PATH': "/home/pycti/test",
    }

    @classmethod
    def load_data(cls, path=CONFIG['DEFAULT_ON_ACCESS_SCAN_LOG']):
        # TODO: implement on access scan detection
        return None

    @classmethod
    def run_scan(cls, path=None):

        if path is None:
            path = cls.CONFIG.get('DEFAULT_SCAN_PATH')

        if not path.startswith(cls.CONFIG.get('DEFAULT_SCAN_PATH')):
            flash("Due to security reasons, the path must start with {}".format(cls.CONFIG.get('DEFAULT_SCAN_PATH')), "error")
            return []

        events = []
        try:
            clam = clamd.ClamdUnixSocket()
            files = clam.multiscan(path)
            for file in files:
                result = files[file][0]
                msg = files[file][1]

                if result == 'FOUND':
                    event = HostEvent(cls.__name__)
                    event.file = file
                    event.signature = msg
                    events.append(event)
                    flash("Found {} in file {}!".format(msg, file), "warning")

                elif result == 'ERROR':
                    flash("Error in file {}: {}".format(file, msg), "error")

                elif result == 'OK':
                    flash("Nothing found in path/file: {}".format(file), "success")

                else:
                    print("ClamAV: unhandled result in file {}: {}, Msg: {}".format(file, result, msg))

        except Exception:
            flash(traceback.format_exc(0), "error")

        return events
