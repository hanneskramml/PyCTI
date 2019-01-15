from flask import redirect, url_for, flash, abort
from core import db, utils
from core.bom import CTI, CTI_STATUS, Actor
from modules.classification import bp
from .decision_tree import DecisionTree


@bp.route('/<module>/<ctiId>')
def classify_features(module, ctiId):
    cti = CTI.query.filter_by(id=ctiId).first_or_404()
    features = utils.get_features_from_cti(cti)

    if module == 'DecisionTree':
        target = DecisionTree.classify_features(features)
    else:
        return abort(404)

    actor = Actor.query.get_or_404(int(target[0]))
    cti.classified_actors.append(actor)

    cti.status = CTI_STATUS['CLASSIFIED']
    db.session.add(cti)
    db.session.commit()

    flash("{} Features have been classified via {}".format(features.__len__(), module))
    return redirect(url_for('show_cti', id=cti.id))
