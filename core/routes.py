from flask import flash, render_template
from core import app
from core.bom import CTI


@app.route('/')
def index():
    flash('Hello World!', 'info')
    return render_template('index.html', title='Dashboard')


@app.route('/cti/<id>')
def cti(id):
    cti = CTI.query.filter_by(id=id).first_or_404()
    return


@app.route('/add_cti', methods=['POST'])
def add_cti():
    return
