from flask import flash, redirect, url_for
from core import db
from core.bom import CTI
from modules.input import bp
from .suricata import SuricataIDS

#@bp.route('/suricata/<id>', methods=['POST'])
@bp.route('/suricata/<id>')
def suricata(id):
    cti = CTI.query.filter_by(id=id).first_or_404()
    events = SuricataIDS.get_events()

    for event in events:
        cti.events.append(event)

    db.session.add(cti)
    db.session.commit()

    flash("Events from SuricataIDS successfully loaded!")
    return redirect(url_for('show_cti', id=cti.id))
