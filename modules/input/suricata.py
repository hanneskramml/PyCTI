from idstools import unified2

CONFIG = {
    'MODULE_NAME': "SuricataIDS",
    'INPUT_TYPE': "IDSAlert",
    'DEFAULT_LOG_PATH': "/var/log/suricata",
    'DEFAULT_LOG_FILE': "unified2.alert"
}


def load_data(path=CONFIG['DEFAULT_LOG_PATH'], file=CONFIG['DEFAULT_LOG_FILE']):
    #reader = unified2.FileRecordReader("/Users/Hannes/git/PyCTI/core/modules/unified2.alert")
    reader = unified2.SpoolRecordReader(path, file, follow=True)

    for record in reader:
        if isinstance(record, unified2.Event):
            print("Event:")
        elif isinstance(record, unified2.Packet):
            print("Packet:")
        elif isinstance(record, unified2.ExtraData):
            print("Extra-Data:")
        print(record)

    return
