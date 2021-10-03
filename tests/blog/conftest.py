import pytest
from django.conf import settings
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"]["NAME"] = os.getenv('TEST_DATABASE_NAME')