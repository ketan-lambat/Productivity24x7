import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


# class TestTag:
#     def test_model(self):
#         tag = mixer.blend('base.Tag')
#         assert tag.pk == 1, 'Should create a Tag instance'
#
#     def test_str(self):
#         tag = mixer.blend('base.Tag')
#         assert tag.name == str(tag), 'Should check the tag name'


class TestTask:
    def test_model(self):
        task = mixer.blend('base.Task')
        assert task.pk == task.id, 'Should create a task instance'

    def test_str(self):
        task = mixer.blend('base.Task')
        assert task.title == str(task), 'Should check the task name'
