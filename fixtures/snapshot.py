"""Execusion JSON test snapshots."""

import json
import os

import pytest

__all__ = ['snapshot']

SNAPSHOT_BASE_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)),
                                 '../snapshots')


class Snapshot(object):
    """JSON snapshots for test failures."""

    def __init__(self, base_dir):
        """Set the base directory."""
        self.base_dir = base_dir

    def assert_match(self, value, name):
        """Return True if the snapshots match."""
        snapshot_path = os.path.join(self.base_dir, name)
        snapshot_dir = os.path.dirname(snapshot_path)

        if not os.path.isdir(snapshot_dir):
            os.makedirs(snapshot_dir, 0o755)

        with open(snapshot_path, 'a+') as snapshot_file:
            snapshot_file.seek(0)
            snapshot = snapshot_file.read()
            if snapshot:
                assert value == json.loads(snapshot), \
                       ('Value did not match snapshot.\n\n'
                        'Value:\n\n{value}\n\n'
                        'Snapshot:\n\n{snapshot}'
                        .format(value=value, snapshot=snapshot))
            else:
                snapshot_file.write(json.dumps(value))


@pytest.fixture(scope='session')
def snapshot(request):
    """Return an object that can save and compare snapshots."""
    return Snapshot(SNAPSHOT_BASE_DIR)
