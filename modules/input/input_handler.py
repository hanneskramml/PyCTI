from flask import flash, redirect, url_for, abort
from core import db
from core.bom import CTI
from core.forms import EventsForm
from modules.input import bp
from .suricata import SuricataIDS
from .generic_file import GenericLogFile


@bp.route('/<module>/<ctiId>', methods=['POST'])
def load_events(module, ctiId):
    cti = CTI.query.filter_by(id=ctiId).first_or_404()

    form = EventsForm()
    path = form.path.data
    file = form.file.data

    if not path:
        path = None
    if not file:
        file = None

    if module == SuricataIDS.__name__:
        events = SuricataIDS.get_events(path=path, file=file)
    elif module == GenericLogFile.__name__:
        events = GenericLogFile.get_events(path=path, file=file)
    else:
        return abort(404)

    for event in events:
        cti.events.append(event)

    db.session.add(cti)
    db.session.commit()

    flash("{} Event(s) loaded from {}!".format(events.__len__(), module))
    return redirect(url_for('show_cti', id=cti.id))
