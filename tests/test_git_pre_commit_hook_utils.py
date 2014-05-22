import git_pre_commit_hook_utils as utils
import scripttest
import os
import copy


def test_git_mode():
    m = utils.GitMode('120000')
    assert m.is_symlink()
    assert not m.is_gitlink()


def test_with_empty_repo(tmpdir):
    os_environ = copy.deepcopy(os.environ)
    os_environ['GIT_DIR'] = str(tmpdir)
    os_environ['GIT_WORK_TREE'] = str(tmpdir)
    env = scripttest.TestFileEnvironment(
        str(tmpdir),
        start_clear=False,
        template_path='data',
        environ=os_environ,
    )
    env.writefile('empty_file', content='')
    env.run('git', 'init')
    env.run('git', 'add', 'empty_file')
    files_staged_for_commit = list(utils.files_staged_for_commit())
    assert len(files_staged_for_commit) == 1
    file_at_index = files_staged_for_commit[0]
    assert file_at_index.path == 'empty_file'
    assert file_at_index.contents == ''
    assert file_at_index.size == 0
    assert file_at_index.status == 'A'


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


def test_is_fnmatch():
    file_at_index = utils.FileAtIndex(
        contents='some text with python\n',
        size=0,
        mode='',
        sha1='',
        status='',
        path='some/path/not_python_script.cpp',
    )
    assert file_at_index.is_fnmatch('*.cpp')
    assert file_at_index.is_fnmatch('*')
    assert not file_at_index.is_fnmatch('*.py')
