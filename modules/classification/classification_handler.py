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
    feature_vect = ts.get_vector_for_features(feature_set)

    if module == 'DecisionTree':
        targets, probs = DecisionTree.classify_features([feature_vect])
    elif module == 'NeuronalNetwork':
        targets, probs = NeuronalNetwork.classify_features([feature_vect])
    else:
        return abort(404)

    for i in range(probs[0].__len__()):
        classification = Classification.query.filter_by(
            cti_id=cti.id, actor_id=ts.target_names[i], source_module=module).first()
        if not classification:
            classification = Classification(source_module=module)
            classification.actor = Actor.query.filter_by(id=ts.target_names[i]).first()
            cti.classifications.append(classification)

        classification.probability = probs[0][i]

    cti.status = CTI_STATUS['CLASSIFIED']
    db.session.add(cti)
    db.session.commit()

    flash("{} / {} Features have been classified using algorithm {}. Top classified actor: {}"
          .format(cti.features.__len__(), ts.n_features, module, cti.get_top_classification().actor.name))
    return redirect(url_for('show_cti', id=cti.id))
