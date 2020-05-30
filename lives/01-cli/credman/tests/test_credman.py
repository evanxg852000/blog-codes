import pytest
from click.testing import CliRunner
from credman import main, Storage

runner = CliRunner()

class FakePickledb():

    def __init__(self):
        self.db = {}

    def create(self, file):
        return True

    def set(self, key, value):
        self.db[key] = value
        return True

    def get(self, key):
        return self.db[key]
    
    def delete(self, key):
        del self.db[key]

    def exists(self, key):
        return key in self.db

def test_create():
    # wrong invocation
    response  = runner.invoke(main, ['create', ])
    assert response.exit_code != 0
    print(response.output)
    # assert 'Usage' in response.output


def test_storage():
    store = Storage('db.test2', FakePickledb())

    assert store.set('a', 12) == True
    assert store.set('b', 5) == True

    assert store.get('a') == 12

    with pytest.raises(Exception):
        store.delete('v')
