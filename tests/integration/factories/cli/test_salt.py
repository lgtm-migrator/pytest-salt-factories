"""
Test the ``salt`` CLI functionality.
"""
import pytest


@pytest.fixture
def salt_minion_2(salt_master, salt_minion):
    """
    This fixture just configures and starts a salt-minion.
    """
    factory = salt_master.salt_minion_daemon(salt_minion.id + "-2")
    with factory.started():
        yield factory


def test_merged_json_out(salt_cli, salt_minion, salt_minion_2):
    ret = salt_cli.run("test.ping", minion_tgt="*")
    assert ret.returncode == 0, ret
    assert ret.data
    assert salt_minion.id in ret.data
    assert ret.data[salt_minion.id] is True
    assert salt_minion_2.id in ret.data
    assert ret.data[salt_minion_2.id] is True


def test_merged_json_out_disabled(salt_cli, salt_minion, salt_minion_2):
    ret = salt_cli.run("test.ping", minion_tgt="*", merge_json_output=False)
    assert ret.returncode == 0, ret
    assert not ret.data
    assert '"{}": true'.format(salt_minion.id) in ret.stdout
    assert '"{}": true'.format(salt_minion_2.id) in ret.stdout
