from idstools import unified2
from core.bom import NetworkEvent
from . import InputModule


class SuricataIDS(InputModule):

    CONFIG = {
        'DEFAULT_LOG_PATH': "/var/log/suricata",
        'DEFAULT_LOG_FILE': "unified2.alert"
    }

    @classmethod
    def get_events(cls, path=CONFIG['DEFAULT_LOG_PATH'], file=CONFIG['DEFAULT_LOG_FILE']):
        reader = unified2.FileRecordReader("/Users/Hannes/git/PyCTI/modules/input/unified2.alert")
        #reader = unified2.SpoolRecordReader(path, file, follow=True)
        events = []

        for record in reader:
            if isinstance(record, unified2.Event):
                event = NetworkEvent(cls.__name__)
                events.append(event)

                event.src_ip = record['source-ip']
                event.dest_ip = record['destination-ip']
                event.protocol = record['protocol']
                event.src_port = record['sport-itype']
                event.dest_port = record['dport-icode']
                event.signature = record['signature-id']

        return events
