from flask import redirect, url_for, flash, abort
from core import db, ts
from core.bom import CTI, CTI_STATUS, Classification, Actor
from modules.classification import bp
from .decision_tree import DecisionTree
from .neuronal_network import NeuronalNetwork


@bp.route('/<module>/<ctiId>')
def classify_features(module, ctiId):
    cti = CTI.query.filter_by(id=ctiId).first_or_404()

    feature_set = {feature.name: feature.power for feature in cti.features}
    feature_vect = ts.get_vector_from_features(feature_set)

    print(feature_set)

    if module == 'DecisionTree':
        targets, probs = DecisionTree.classify_features([feature_vect])
    elif module == 'NeuronalNetwork':
        targets, probs = NeuronalNetwork.classify_features([feature_vect])
    else:
        return abort(404)

    print(targets)

    for target in targets:
        classification = Classification(source_module=module)
        classification.actor = Actor.query.filter_by(id=int(target)).first()
        cti.classifications.append(classification)

    for probability in probs:
        print(probability)

    cti.status = CTI_STATUS['CLASSIFIED']
    db.session.add(cti)
    db.session.commit()

    flash("{} Features have been classified using algorithm {}.".format(ts.n_features, module))
    return redirect(url_for('show_cti', id=cti.id))
