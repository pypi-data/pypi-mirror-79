import logging

from avatar_utils.sso_helper import SSOHelper
from avatar_utils.tests.UnitTest import UnitTest

logger = logging.getLogger(__name__)

sso = SSOHelper(client_id='client_id')


class BaseUnitTest(UnitTest):
    from app import create_app, db

    app = create_app('testing')
    client = app.test_client()
    db = db

    sso_id = 'test'

    token = None

    def setUp(self):
        super().setUp()

        self.token = sso.make_token(sso_user_id=self.sso_id)

        auth_header = {'Authorization': f'Bearer {self.token}'}
        self.headers = {**self.headers, **auth_header}
