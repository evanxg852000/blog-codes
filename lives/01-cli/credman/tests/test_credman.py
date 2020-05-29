import pytest
from click.testing import CliRunner
from credman import main, Storage



runner = CliRunner()

def test_create():
    # go invocation
    response = runner.invoke(main, ['create', 'valgrind'])
    assert response.exit_code == 0
    assert '[ok]' in response.output

    # wrong invocation
    response = runner.invoke(main, ['create',])
    assert response.exit_code != 0
    assert 'Usage:' in response.output

def test_storage():
    store = Storage('db.test')

    assert store.set('a', 12) == True
    assert store.set('b', 5) == True

    assert store.get('a') == 12

    with pytest.raises(Exception):
        store.delete('v')