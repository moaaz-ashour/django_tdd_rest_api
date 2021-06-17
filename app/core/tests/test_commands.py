from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandsTestCase(TestCase):
    """ we create a command wait_for_db to check if database is
    available before running server. Here we test if this command"""

    def test_wait_for_db_ready(self):
        """check if the command wait_for_db works when db is available
            by simulating the behaviour of Django when
            db is available
        """
        # Mock ConnectionHandler with Patch to return True everytime the command is called
        # The way to test if db is available in Django is by retrieving the default db via the ConnectionHandler
        # THe fucntion which is called when retrieving the db is __getitem__
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # mocking/ overriding behaviour
            gi.return_value = True
            call_command('wait_for_db')
            # check if __getitem__ is called once
            self.assertEqual(gi.call_count, 1)

    # The command will check if the ConnectionHandler raises an error
    # if it does, it is going to wait a second and then try again
    # to remove that delay, wrap the test in a @patch decorator
    # to not sleep for the test
    @patch('time.sleep', return_value=None)
    def test_wait_for_db(self, ts): 
        """Test wait_for_db command will try the db 5 times
            on the sixth time will be successful
            ts: from the patch decorator.
        """
        # make the patch return error for first five calls
        # and return true on sixth call
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)