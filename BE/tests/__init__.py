import os
from app.infrastructure.postgresql import init_db

os.putenv("ENV", "test")

init_db(show_logs=True, test=True)


class FunctionalTestCase:

    def boot(self):
        pass
