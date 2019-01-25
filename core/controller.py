from flask import flash, render_template, redirect, url_for
from core import app, db, rulemanager, utils
from core.bom import CTI, CTI_STATUS, Feature, Actor
from core.forms import AddForm


@app.route('/', methods=['GET'])
def index():
    ctiList = CTI.query.filter(CTI.status != CTI_STATUS['ARCHIVED']).order_by(CTI.id.desc()).all()

    # TODO: Implement dashboard view

    return render_template('index.html', ctiList=ctiList)


@app.route('/add_cti', methods=['GET', 'POST'])
def add_cti():
    form = AddForm()
    if form.validate_on_submit():
        cti = CTI(str(form.name.data))

        db.session.add(cti)
        db.session.commit()

        return redirect(url_for('show_cti', id=cti.id))

    return render_template('add.html', form=form)


@app.route('/cti/<id>/delete', methods=['POST'])
def delete_cti(id):
    cti = CTI.query.get_or_404(id)

    db.session.delete(cti)
    db.session.commit()

    flash("CTI deleted: {} ({})".format(cti.name, cti.id))
    return redirect(url_for('index'))


@app.route('/cti/<id>/archive', methods=['POST'])
def archive_cti(id):
    cti = CTI.query.get_or_404(id)

    cti.status = CTI_STATUS['ARCHIVED']
    db.session.add(cti)
    db.session.commit()

    flash("CTI archived: {} ({})".format(cti.name, cti.id))
    return redirect(url_for('index'))


@app.route('/archive', methods=['GET'])
def archive():
    ctiList = CTI.query.filter_by(status=CTI_STATUS['ARCHIVED']).order_by(CTI.id.desc()).all()

    return render_template('archive.html', ctiList=ctiList)


@app.route('/features', methods=['GET'])
def features():
    featList = Feature.query.order_by(Feature.id.asc()).all()

    return render_template('features.html', featList=featList)


@app.route('/feature/<id>', methods=['GET'])
def show_feat(id):
    feat = Feature.query.get_or_404(id)
    return render_template('feature.html', feat=feat)


@app.route('/actors', methods=['GET'])
def actors():
    actList = Actor.query.order_by(Actor.id.asc()).all()

    return render_template('actors.html', actList=actList)


@app.route('/actor/<id>', methods=['GET'])
def show_act(id):
    act = Actor.query.get_or_404(id)
    return render_template('actor.html', act=act)


@app.route('/cti/<id>', methods=['GET'])
def show_cti(id):
    cti = CTI.query.get_or_404(id)
    return render_template('cti.html', cti=cti)


@app.route('/cti/<id>/analyse_events')
def analyse_events(id):
    cti = CTI.query.get_or_404(id)
    features = Feature.query.all()
    n_matches = 0

    for event in cti.events:
        str_obj = utils.get_dict_from_object(event).__str__()
        matches = rulemanager.match_data(str_obj)

        for match in matches:
            for key in match.meta:

                try:
                    index = features.index(match.meta[key])

                    event.analysed_features.append(features[index])
                    cti.features.append(features[index])
                    n_matches += 1

                except ValueError:
                    print("WARNING for Event=>Feature mapping: Feature '{}' specified in yara rule {} ({}) not found!"
                          .format(match.meta[key], match.rule, match.namespace))

    cti.status = CTI_STATUS['ANALYSED']
    db.session.add(cti)
    db.session.commit()

    flash("{} CTI Event(s) analysed! Found {} distinct feature(s) in {} rule match(es)."
          .format(cti.events.__len__(), cti.features.__len__(), n_matches))

    return redirect(url_for('show_cti', id=cti.id))


@app.route('/cti/<id>/export_cti')
def export_cti(id):
    cti = CTI.query.get_or_404(id)
    flash("STIX export / TAXI sharing not yet implemented!", 'error')
    return redirect(url_for('show_cti', id=cti.id))
