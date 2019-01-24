import pyclamd
from modules.input import InputModule


class ClamAV(InputModule):

    CONFIG = {
        'MODULE_NAME': "ClamAV",
        'DEFAULT_ON_ACCESS_SCAN_LOG': "/var/log/clamav/infected.log",
        'DEFAULT_SCAN_PATH': "/home"
    }

    clam = None

    @classmethod
    def connect(cls):
        try:
            cls.clam = pyclamd.ClamdUnixSocket()
            cls.clam.ping()
        except pyclamd.ConnectionError:
            # if failed, test for network socket
            try:
                cls.clam = pyclamd.ClamdNetworkSocket()
                cls.clam.ping()
            except pyclamd.ConnectionError:
                raise ValueError('Unable not connect to ClamdAV server either by unix or network socket')

    @classmethod
    def load_data(cls, path=CONFIG['DEFAULT_ON_ACCESS_SCAN_LOG']):
        # TODO: implement on access scan detection
        return

    @classmethod
    def run_scan(cls, path=CONFIG['DEFAULT_SCAN_PATH']):
        return


ClamAV.connect()
print("Connection to ClamAV server established")
