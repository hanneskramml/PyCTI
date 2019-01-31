import mysql.connector, traceback
from datetime import datetime
from flask import flash

from core.bom import NetworkEvent
from modules.input import InputModule


class SuricataIDS(InputModule):

    CONFIG = {
        'MYSQL_HOST': "localhost",
        'MYSQL_DB': "suricata",
        'MYSQL_USER': "",
        'MYSQL_PASS': "",
        'MYSQL_QUERY':
            "SELECT timestamp, sip, dip, sport, dport, protocol, priority, signatureName, className FROM idsDataStore_1000_Events WHERE eventID is not null ORDER BY timestamp desc",
        'DEFAULT_QUERY_LIMIT': 10000
    }

    @classmethod
    def get_events(cls, path=None, file=None, limit=None):

        if limit is None:
            limit = cls.CONFIG.get("DEFAULT_QUERY_LIMIT")

        events = []
        try:
            db = mysql.connector.connect(
                host=cls.CONFIG.get("MYSQL_HOST"),
                database=cls.CONFIG.get("MYSQL_DB"),
                user=cls.CONFIG.get("MYSQL_USER"),
                passwd=cls.CONFIG.get("MYSQL_PASS")
            )

            cursor = db.cursor()
            cursor.execute(cls.CONFIG.get("MYSQL_QUERY"))

            result = cursor.fetchmany(limit)
            for record in reversed(result):

                event = NetworkEvent(source_module=cls.__name__)
                events.append(event)

                if record[0]:
                    event.timestamp = datetime.fromtimestamp(record[0])
                event.src_ip = record[1] if record[1] else None
                event.dest_ip = record[2] if record[2] else None
                event.src_port = record[3] if record[3] else None
                event.dest_port = record[4] if record[4] else None
                event.protocol = record[5] if record[5] else None
                event.signature = record[7] if record[7] else None
                event.reference = record[8] if record[8] else None

            db.close()

        except Exception:
            flash(traceback.format_exc(0), "error")

        return events
