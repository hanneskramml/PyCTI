from flask import flash, render_template
from core import app, db
from core.bom import CTI


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

    return render_template('cti.html', cti=cti)


@app.route('/cti/<id>', methods=['GET'])
def show_cti(id):
    cti = CTI.query.get_or_404(id)
    return render_template('cti.html', cti=cti)

