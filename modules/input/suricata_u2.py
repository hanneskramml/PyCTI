import json
from idstools import unified2, maps
from flask import flash

from core.bom import NetworkEvent
from modules.input import InputModule


class SuricataIDS(InputModule):

    CONFIG = {
        'DEFAULT_LOG_PATH': "/var/log/suricata",
        'DEFAULT_LOG_FILE': "unified2.alert",
        'GEN_MAP_PATH': "/etc/suricata/rules/gen-msg.map",
        'SIG_MAP_PATH': "/etc/suricata/rules/sid-msg.map"
    }

    @classmethod
    def get_events(cls, path=None, file=None):

        if path is None:
            path = cls.CONFIG['DEFAULT_LOG_PATH']

        if file is None:
            file = cls.CONFIG['DEFAULT_LOG_FILE']

        events = []

        try:
            sigmap = maps.SignatureMap()
            sigmap.load_generator_map(open(cls.CONFIG.get('GEN_MAP_PATH')))
            sigmap.load_signature_map(open(cls.CONFIG.get('SIG_MAP_PATH')))

            reader = unified2.SpoolRecordReader(path, file, follow=False)

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

        except Exception as e:
            flash(e.__class__.__name__, "error")

        return events
