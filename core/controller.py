from flask import flash, render_template, redirect, url_for
from core import app, db, rulemanager, utils
from core.bom import CTI, CTI_STATUS, Feature
from core.forms import AddForm


@app.route('/', methods=['GET'])
def index():
    ctiList = CTI.query.order_by(CTI.timestamp.desc()).all()

    # TODO: Implement dashboard view

    return render_template('index.html', ctiList=ctiList)


# @app.route('/add_cti', methods=['POST'])
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


@app.route('/cti/<id>', methods=['GET'])
def show_cti(id):
    cti = CTI.query.get_or_404(id)
    labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
    return render_template('cti.html', cti=cti, labels=labels)


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
