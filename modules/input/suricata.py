import json
from idstools import unified2, maps

from core.bom import NetworkEvent
from modules.input import InputModule


class SuricataIDS(InputModule):

    CONFIG = {
        'DEFAULT_LOG_PATH': "/var/log/suricata",
        'DEFAULT_LOG_FILE': "unified2.alert",
        'GEN_MAP_PATH': "/Users/Hannes/git/PyCTI/modules/input/gen-msg.map",
        'SIG_MAP_PATH': "/Users/Hannes/git/PyCTI/modules/input/sid-msg.map"
    }

    @classmethod
    def get_events(cls, path=CONFIG['DEFAULT_LOG_PATH'], file=CONFIG['DEFAULT_LOG_FILE']):

        sigmap = maps.SignatureMap()
        sigmap.load_generator_map(open(cls.CONFIG.get('GEN_MAP_PATH')))
        sigmap.load_signature_map(open(cls.CONFIG.get('SIG_MAP_PATH')))

        reader = unified2.FileRecordReader("/Users/Hannes/git/PyCTI/modules/input/unified2.alert")
        #reader = unified2.SpoolRecordReader(path, file, follow=True)
        events = []

        for record in reader:
            if isinstance(record, unified2.Event):

                event_details = sigmap.get(record['generator-id'], record['signature-id'])

                event = NetworkEvent(cls.__name__)
                events.append(event)

                event.src_ip = record['source-ip']
                event.dest_ip = record['destination-ip']
                event.protocol = record['protocol']
                event.src_port = record['sport-itype']
                event.dest_port = record['dport-icode']
                event.signature = event_details['msg'] if event_details else 'SID: {}'.format(record['signature-id'])
                if event_details:
                    event.reference = json.dumps(event_details['ref'])

        return events
