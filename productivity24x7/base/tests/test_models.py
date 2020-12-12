import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestTask:
    def test_model(self):
        task = mixer.blend('base.Task')
        assert task.pk == task.id, 'Should create a task instance'

    def test_str(self):
        task = mixer.blend('base.Task')
        assert task.title == str(task), 'Should check the task name'
