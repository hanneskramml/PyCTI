from flask import flash, render_template, redirect, url_for
from core import app, db, rulemanager, utils
from core.bom import CTI, CTI_STATUS, Software, Behaviour
from core.forms import AddForm, DeleteForm


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

    # TODO: Implement dashboard view

    return render_template('index.html', title='PyCTI')


# TODO: Implement form for CTI creation
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


@app.route('/delete_cti/<id>', methods=['GET'])
def delete_cti(id):
    form = DeleteForm()

    return render_template('delete.html', cti=CTI.query.get_or_404(id), form=form)


@app.route('/delete_cti/<id>/4ever', methods=['POST'])
def delete_cti_4ever(id):
    cti = CTI.query.get_or_404(id)

    db.session.delete(cti)
    db.session.commit()

    return redirect('cti_tab')


@app.route('/cti_tab', methods=['GET'])
def cti_tab():
    ctiList = CTI.query.order_by(CTI.timestamp.desc()).all()

    return render_template('cti_tab.html', ctiList=ctiList)


@app.route('/cti/<id>', methods=['GET'])
def show_cti(id):
    cti = CTI.query.get_or_404(id)
    return render_template('cti.html', cti=cti)


# @app.route('/cti/<id>/analyse_events', methods=['POST'])
@app.route('/cti/<id>/analyse_events')
def analyse_events(id):
    cti = CTI.query.get_or_404(id)

    stats_sw = 0
    stats_tec = 0

    for event in cti.events:
        str_obj = utils.get_dict_from_object(event).__str__()
        matches = rulemanager.match_data(str_obj)

        for match in matches:
            for feature in match.meta:
                if "software" in feature:
                    software = db.session.query(Software).filter_by(name=match.meta[feature]).first()
                    if software:
                        event.analysed_software.append(software)
                        stats_sw += 1

                else:
                    behaviour = db.session.query(Behaviour).filter_by(name=match.meta[feature]).first()
                    if behaviour:
                        event.analysed_behaviours.append(behaviour)
                        stats_tec += 1

                db.session.add(event)

    cti.status = CTI_STATUS['ANALYSED']
    db.session.add(cti)
    db.session.commit()

    flash("{} CTI Event(s) analysed! Found {} Software and {} behavioural match(es)."
          .format(cti.events.__len__(), stats_sw, stats_tec))

    return redirect(url_for('show_cti', id=cti.id))
