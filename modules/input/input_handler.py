from flask import flash, redirect, url_for, abort
from core import db
from core.bom import CTI
from modules.input import bp
from .suricata import SuricataIDS
from .generic_file import GenericLogFile


@bp.route('/<module>/<ctiId>', methods=['POST'])
def load_events(module, ctiId):
    cti = CTI.query.filter_by(id=ctiId).first_or_404()

    if module == SuricataIDS.__name__:
        events = SuricataIDS.get_events()
    elif module == GenericLogFile.__name__:
        events = GenericLogFile.get_events()
    else:
        return abort(404)

    for event in events:
        cti.events.append(event)

    db.session.add(cti)
    db.session.commit()

    flash("{} Events from {} successfully loaded!".format(events.__len__(), module))
    return redirect(url_for('show_cti', id=cti.id))
