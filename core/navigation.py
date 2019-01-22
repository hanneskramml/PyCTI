from flask_nav.elements import Navbar, View
from core import nav


@nav.navigation()
def mynavbar():
    return Navbar(
        'PyCTI',
        View('Dashboard', 'index'),
        View('New', 'add_cti'),
    )
