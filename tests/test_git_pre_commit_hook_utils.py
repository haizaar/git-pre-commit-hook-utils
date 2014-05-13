import git_pre_commit_hook_utils as utils


def test_is_python_code_by_path():
    file_at_index = utils.FileAtIndex(
        contents='',
        size=0,
        mode='',
        sha1='',
        status='',
        path='some/path/main.py',
    )
    assert file_at_index.is_python_code()


def test_is_python_code_by_contents():
    file_at_index = utils.FileAtIndex(
        contents='#!/usr/bin/env/python\nprint "hello"\n',
        size=0,
        mode='',
        sha1='',
        status='',
        path='some/path/python_script',
    )
    assert file_at_index.is_python_code()


def test_is_not_python_code():
    file_at_index = utils.FileAtIndex(
        contents='some text with python\n',
        size=0,
        mode='',
        sha1='',
        status='',
        path='some/path/not_python_script.cpp',
    )
    assert not file_at_index.is_python_code()
