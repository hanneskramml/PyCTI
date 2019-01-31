from flask import flash, redirect, url_for, abort, request
from core import db
from core.bom import CTI
from core.forms import EventsForm
from modules.input import bp
from .suricata_db import SuricataIDS
from .clamav import ClamAV
from .generic_file import GenericLogFile


@bp.route('/<module>/<ctiId>', methods=['POST'])
def load_events(module, ctiId):
    cti = CTI.query.filter_by(id=ctiId).first_or_404()
    form = EventsForm()

    path = form.path.data
    file = form.file.data
    limit = form.limit.data

    if not path:
        path = None
    if not limit:
        limit = None

    if 'file' in request.files and file.filename != '':
        file = request.files['file']
    else:
        file = None

    if module == SuricataIDS.__name__:
        events = SuricataIDS.get_events(limit=limit)
    elif module == ClamAV.__name__:
        events = ClamAV.run_scan(path=path)
    elif module == GenericLogFile.__name__:
        events = GenericLogFile.get_events(file=file)
    else:
        return abort(404)

    for event in events:
        cti.events.append(event)

    db.session.add(cti)
    db.session.commit()

    flash("{} Event(s) loaded from {}!".format(events.__len__(), module))
    return redirect(url_for('show_cti', id=cti.id))
