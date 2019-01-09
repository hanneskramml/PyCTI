from flask import flash, render_template, redirect, url_for
from core import app, db, rulemanager, utils
from core.bom import CTI, CTI_STATUS, Software, Technique


@app.route('/', methods=['GET'])
def index():

    # TODO: Implement dashboard view
    flash('Hello World!', 'info')

    return render_template('index.html')


# TODO: Implement modal form for CTI creation
# @app.route('/add_cti', methods=['POST'])
@app.route('/add_cti', methods=['GET', 'POST'])
def add_cti():
    cti = CTI("TestCTI")

    db.session.add(cti)
    db.session.commit()

    return redirect(url_for('show_cti', id=cti.id))


@app.route('/cti/<id>', methods=['GET'])
def show_cti(id):
    cti = CTI.query.get_or_404(id)
    return render_template('cti.html', cti=cti)


# @app.route('/cti/<id>/analyse_events', methods=['POST'])
@app.route('/cti/<id>/analyse_events')
def analyse_events(id):
    cti = CTI.query.get_or_404(id)

    for event in cti.events:

        event_str = utils.get_dict_from_object(event).__str__()
        sw_match = rulemanager.match_software(event_str)
        tec_match = rulemanager.match_techniques(event_str)

        for match in sw_match:
            for feature in match.meta:
                software = Software.query.filter_by(name=match.meta[feature]).first()
                if software:
                    event.analysed_software.append(software)

        for match in tec_match:
            for feature in match.meta:
                technique = Technique.query.filter_by(name=match.meta[feature]).first()
                if technique:
                    event.analysed_techniques.append(technique)

    cti.status = CTI_STATUS['ANALYSED']
    db.session.add(cti)
    db.session.commit()

    flash("CTI Events analysed successfully!")

    return redirect(url_for('show_cti', id=cti.id))
