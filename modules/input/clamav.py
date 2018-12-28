import pyclamd

CONFIG = {
    'MODULE_NAME': "ClamAV",
    'INPUT_TYPE': "MalwareDetection",
    'DEFAULT_ON_ACCESS_SCAN_LOG': "/var/log/clamav/infected.log",
    'DEFAULT_SCAN_PATH': "/home"
}


def _connect():
    try:
        clam = pyclamd.ClamdUnixSocket()
        clam.ping()
    except pyclamd.ConnectionError:
        # if failed, test for network socket
        clam = pyclamd.ClamdNetworkSocket()
        try:
            clam.ping()
        except pyclamd.ConnectionError:
            raise ValueError('Unable not connect to ClamdAV server either by unix or network socket')
    return clam


def load_data(path=CONFIG['DEFAULT_ON_ACCESS_SCAN_LOG']):
    print(path)
    return


def run_scan(path=CONFIG['DEFAULT_SCAN_PATH']):
    _connect()
    return