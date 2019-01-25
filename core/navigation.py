from flask_nav.elements import Navbar, View
from core import nav


@nav.navigation()
def mynavbar():
    return Navbar(
        'PyCTI',
        View('Dashboard', 'index'),
        View('CTIs', 'ctis'),
        View('Features', 'features'),
        View('Actors', 'actors'),
    )
