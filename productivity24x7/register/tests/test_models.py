import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestUser:
    def test_model(self):
        user = mixer.blend('register.User')
        assert user.pk == 1, 'Should create a Tag instance'
