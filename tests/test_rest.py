from unittest import TestCase
from tic_tac_toe import app, log

logger = log.getLogger()
log.set_verbosity(log.DEBUG)

class TestRest(TestCase):
    
    @classmethod
    def setUpClass(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()


    def test_hello(self):
        rv = self.app.get('/')
        assert(rv.data.decode() == 'Tic Tac Toe by Ramon Medeiros')

