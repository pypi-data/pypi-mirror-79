#!/usr/bin/env python

"""Tests for the utils module."""

import pytest

from db_faker.lib import utils


# Get the absolute path of the current directory
current_absolute_path = utils.get_root_path() / 'tests'


@pytest.mark.parametrize("path, expected", [
    (str(current_absolute_path / 'sample-schema.json'), True),
    ("./sample-schema.json", True),
    (str(current_absolute_path / 'invalid-file.txt'), False),
    ("./invalid-file.txt", False)])
def test_is_file(path: str, expected):
    """
    Tests files exists in unix platforms
    """
    file_exists = utils.file_exists(path)

    assert file_exists == expected
